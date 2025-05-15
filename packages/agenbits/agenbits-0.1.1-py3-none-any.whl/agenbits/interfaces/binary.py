from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file

def Binary(path_or_url: str) -> bytes:
    if path_or_url.startswith("http"):
        data = fetch_data_from_url(path_or_url)
        file_path = save_binary_file(data)
    else:
        file_path = path_or_url

    return load_binary_file(file_path)
