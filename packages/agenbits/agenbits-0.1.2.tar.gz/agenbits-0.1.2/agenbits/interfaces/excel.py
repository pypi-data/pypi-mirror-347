import os
import io
import pandas as pd

from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file

def Excel(path_or_url: str, file_type: str = None):
    if path_or_url.startswith("http"):
        raw_data = fetch_data_from_url(path_or_url)
        binary_path = save_binary_file(raw_data, filename="excel_input.bin")
    else:
        with open(path_or_url, "rb") as f:
            raw_data = f.read()
        binary_path = save_binary_file(raw_data, filename="excel_input.bin")

    file_bytes = load_binary_file(binary_path)

    if os.path.exists(binary_path):
        os.remove(binary_path)

    bytes_io = io.BytesIO(file_bytes)

    # Auto-detect if file_type is not provided
    if not file_type:
        if path_or_url.endswith(".csv"):
            file_type = "csv"
        elif path_or_url.endswith(".xlsx") or path_or_url.endswith(".xls"):
            file_type = "excel"
        else:
            file_type = "csv"  # default fallback

    if file_type.lower() == "csv":
        df = pd.read_csv(bytes_io)
    elif file_type.lower() in ["xlsx", "excel"]:
        df = pd.read_excel(bytes_io)
    else:
        raise ValueError(f"Unsupported Excel file type: {file_type}")

    return df
