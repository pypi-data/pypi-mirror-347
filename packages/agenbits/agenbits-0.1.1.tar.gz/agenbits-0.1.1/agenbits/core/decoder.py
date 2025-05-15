def load_binary_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()
