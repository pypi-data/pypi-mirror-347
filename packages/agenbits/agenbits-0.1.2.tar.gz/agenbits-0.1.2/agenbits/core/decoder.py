import os

def load_binary_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        data = f.read()
    os.remove(file_path)  # Clean up temp file immediately after reading
    return data
