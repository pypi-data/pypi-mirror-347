import os

from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file

def Video(path_or_url: str):
    if path_or_url.startswith("http"):
        raw_data = fetch_data_from_url(path_or_url)
        binary_path = save_binary_file(raw_data, filename="video_input.bin")
    else:
        with open(path_or_url, "rb") as f:
            raw_data = f.read()
        binary_path = save_binary_file(raw_data, filename="video_input.bin")

    # For video, often ML models take a file path, so just return the path

    if os.path.exists(binary_path):
        # We can't delete immediately or user won't be able to use the path
        # Instead, user should delete it after processing or we can provide a cleanup method
        pass

    return binary_path
