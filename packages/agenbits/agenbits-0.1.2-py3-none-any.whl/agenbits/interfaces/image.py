from PIL import Image
import io
import os

from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file
from agenbits.core.detector import detect_file_type_from_url

def ImageFile(path_or_url: str):
    # Step 1: Fetch and save as .bin
    if path_or_url.startswith("http"):
        raw_data = fetch_data_from_url(path_or_url)
        binary_path = save_binary_file(raw_data, filename="image_input.bin")
    else:
        with open(path_or_url, "rb") as f:
            raw_data = f.read()
        binary_path = save_binary_file(raw_data, filename="image_input.bin")

    # Step 2: Decode the binary into an image
    image_bytes = load_binary_file(binary_path)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Step 3: Auto-delete the temp binary
    if os.path.exists(binary_path):
        os.remove(binary_path)

    return image
