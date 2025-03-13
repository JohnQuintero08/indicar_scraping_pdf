#!/bin/bash

# Verifica si se proporcionó un argumento (ruta de la carpeta)
if [ -z "$1" ]; then
    echo "Error: You must provide a folder path with PDFs"
    exit 1
fi

# Ruta del script de Python
SCRIPT_PYTHON="./scraping.py"

# Ejecutar Python pasando la ruta como argumento
python "$SCRIPT_PYTHON" "$1"

