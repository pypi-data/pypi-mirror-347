import cv2
import numpy as np
from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file
from agenbits.core.detector import detect_file_type_from_url


def Video(path_or_url: str):
    if path_or_url.startswith("http"):
        raw_data = fetch_data_from_url(path_or_url)
        binary_path = save_binary_file(raw_data)

        # Check if the file is indeed a video
        file_type = detect_file_type_from_url(path_or_url)
        if "video" not in file_type:
            raise ValueError(f"The URL does not point to a video file. Detected type: {file_type}")

        return binary_path  # Path to the saved video file
    else:
        raise ValueError("Currently, only URL-based video sources are supported.")
