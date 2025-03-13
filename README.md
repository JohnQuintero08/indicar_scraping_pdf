# **IndyCar Report Scraper**

## **Project Overview**
This script performs **scraping of session reports** for **IndyCar drivers**. It extracts all the relevant data from the reports and organizes it into **Pandas DataFrames**, using the `pdfplumber` library to process the **PDF files**.

The script can be executed from a **Bash terminal** or manually within a **Python environment**.

---

## **Usage**

### **1️⃣ Running from Bash**
To execute the script from a **Bash terminal**, navigate to the project folder and run:
```bash
./run_script.sh "pdfs"
```

🔹 **Parameters:**
- `run_script.sh`: The script to be executed.
- `pdfs`: The folder where the PDF reports are stored.

🔹 **Execution Flow:**
- The script will extract tables and headers from each PDF.
- The **progress of each file** will be displayed in the terminal.
- The **last page of the main PDF is not extracted**—only driver-specific session data is processed.
- A folder named **`new_datasets/`** will be created automatically, where the extracted datasets will be saved in **Parquet format**.

---

### **2️⃣ Running Manually in Python**
If you prefer to execute the process manually within Python, use the following function:
```python
read_and_save_dataset("./pdfs")
```

🔹 **Parameter:**
- A **string** representing the path to the folder containing the PDFs.

This function will read all PDF reports, process their data, and save them as **Parquet** files in the `new_datasets/` directory.

---

## **Requirements**
Ensure you have the required dependencies installed. You can install them using:
```bash
pip install -r requirements.txt
```

---

Enjoy! 🚀

