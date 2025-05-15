import pandas as pd
from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file
from agenbits.core.detector import detect_file_type_from_url

def Excel(path_or_url: str, type: str = None) -> pd.DataFrame:
    if path_or_url.startswith("http"):
        data = fetch_data_from_url(path_or_url)
        file_path = save_binary_file(data)
    else:
        file_path = path_or_url

    ext = type or detect_file_type_from_url(path_or_url).split("/")[-1]
    content = load_binary_file(file_path)

    if "csv" in ext:
        return pd.read_csv(file_path)
    elif "excel" in ext or "xlsx" in ext:
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported Excel file type")
