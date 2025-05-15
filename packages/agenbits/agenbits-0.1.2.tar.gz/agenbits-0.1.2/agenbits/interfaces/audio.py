import io
import os
import soundfile as sf
import numpy as np

from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file

def Audio(path_or_url: str):
    if path_or_url.startswith("http"):
        raw_data = fetch_data_from_url(path_or_url)
        binary_path = save_binary_file(raw_data, filename="audio_input.bin")
    else:
        with open(path_or_url, "rb") as f:
            raw_data = f.read()
        binary_path = save_binary_file(raw_data, filename="audio_input.bin")

    audio_bytes = load_binary_file(binary_path)

    # Load audio from bytes
    with io.BytesIO(audio_bytes) as audio_io:
        data, samplerate = sf.read(audio_io)

    if os.path.exists(binary_path):
        os.remove(binary_path)

    # Return audio data as numpy array + samplerate (common ML input)
    return data, samplerate
