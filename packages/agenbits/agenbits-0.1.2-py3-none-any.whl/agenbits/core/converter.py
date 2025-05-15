from pathlib import Path

def save_binary_file(data: bytes, filename: str = "input_file.bin") -> Path:
    temp_path = Path("tempdata") / filename
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(data)
    return temp_path
