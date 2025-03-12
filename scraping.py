import pandas as pd
import pdfplumber
import re
import numpy as np
pd.set_option('future.no_silent_downcasting', True)


def extract_text(script, text):
    return re.search(script, text).group(1)


def extract_header(page):
    text = page.extract_text()
    event = extract_text(r'Event:\s*(.*?)\s*Round', text)
    round = extract_text(r'Round\s*(.*?)\s*Track', text)
    track = extract_text(r'Track:\s*(.*?)\s*Report', text)
    report = extract_text(r'Report:\s*(.*?)\s*Session', text)
    session = extract_text(r'Session:\s*(.*?)\s*\n', text)
    car, driver = extract_text(r'Car\s*(.*?)\s*\n', text).split('-')
    return event, round, track, report, session, car, driver


def extract_table(page):
    table = np.array(page.extract_table())
    return table


def print_header(header):
    event, round, track, report, session, car, driver = header
    result = f"""
    Event: {event}
    Round: {round}
    Track: {track}
    Report: {report}
    Session: {session}
    Car: {car}
    Driver: {driver}
    """
    print(result)


def full_array(size, param):
    return np.full(size, param)


def lap_correction(lap_list):
    new_list = []
    for i in range(len(lap_list)):
        j = lap_list.iloc[i]
        if i == 0:
            valor = j
        elif i % 2 == 1:
            valor = lap_list.iloc[i-1]
        else:
            valor = j
        new_list.append(valor)
    return new_list


def table_correction(df):
    df['Lap'] = lap_correction(df['Lap'])
    df = df.replace('', np.nan)

    integer_columns = ['car', 'Lap']
    float_columns = ['SF_to_T1', 'T1_to_SS1', 'SS1_to_T2', 'T2_to_BS', 'BS_to_T3', 'T3_to_SS2',
                     'SS2_to_T4', 'T4_to_FS', 'FS_to_SF', 'Lapt', 'PI_to_PO', 'PO_to_SF', 'SF_to_PI']
    for col in integer_columns:
        df[col] = df[col].astype(int)
    for col in float_columns:
        df[col] = df[col].astype(float)

    return df


def create_df_page(page):
    header = extract_header(page)
    table = extract_table(page)
    headers_table = ['Lap', 'T/S', 'SF_to_T1', 'T1_to_SS1', 'SS1_to_T2', 'T2_to_BS', 'BS_to_T3',
                     'T3_to_SS2', 'SS2_to_T4', 'T4_to_FS', 'FS_to_SF', 'Lapt', 'PI_to_PO', 'PO_to_SF', 'SF_to_PI']
    shape_table = np.shape(table)[0]
    event, round, track, report, session, car, driver = header

    event_arr = full_array(shape_table, event)
    round_arr = full_array(shape_table, round)
    track_arr = full_array(shape_table, track)
    report_arr = full_array(shape_table, report)
    session_arr = full_array(shape_table, session)
    car_arr = full_array(shape_table, car)
    driver_arr = full_array(shape_table, driver)

    data = {'event': event_arr,
            'round': round_arr,
            'track': track_arr,
            'report': report_arr,
            'session': session_arr,
            'car': car_arr,
            'driver': driver_arr}

    df_header = pd.DataFrame(data)
    df_table = pd.DataFrame(table, columns=headers_table)
    df_page = pd.concat([df_header, df_table], axis=1)

    df_page_corrected = table_correction(df_page)

    return df_page_corrected


def read_all_pages(pdf):
    base_df = create_df_page(pdf.pages[0])
    for page in range(1, len(pdf.pages)):
        print(f'Reading page {page}')
        try:
            new_df = create_df_page(pdf.pages[page])
            base_df = pd.concat([base_df, new_df],
                                axis=0).reset_index(drop=True)
        except:
            print(
                f'Page # {page+1} was not read it has different content to the format')
            continue
    print('No more pages to read ... we are done')
    return base_df

# Example for use the functions
#   pdf =  pdfplumber.open('doc_1.pdf')
#   whole_pdf = read_all_pages(pdf)
