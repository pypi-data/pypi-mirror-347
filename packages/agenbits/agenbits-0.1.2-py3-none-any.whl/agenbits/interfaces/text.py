import os
import io
import json

from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file

def Text(path_or_url: str, file_type: str = None):
    if path_or_url.startswith("http"):
        raw_data = fetch_data_from_url(path_or_url)
        binary_path = save_binary_file(raw_data, filename="text_input.bin")
    else:
        with open(path_or_url, "rb") as f:
            raw_data = f.read()
        binary_path = save_binary_file(raw_data, filename="text_input.bin")

    file_bytes = load_binary_file(binary_path)

    if os.path.exists(binary_path):
        os.remove(binary_path)

    text_str = file_bytes.decode("utf-8")

    # Auto-detect file type or fallback to plain text
    if not file_type:
        if path_or_url.endswith(".json"):
            file_type = "json"
        elif path_or_url.endswith(".xml"):
            file_type = "xml"
        else:
            file_type = "txt"

    if file_type == "json":
        return json.loads(text_str)
    elif file_type == "xml":
        # You could add XML parsing here if needed
        return text_str
    else:
        return text_str
