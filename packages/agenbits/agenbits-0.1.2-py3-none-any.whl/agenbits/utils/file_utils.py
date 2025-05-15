import os
from pathlib import Path

def get_extension_from_url(url: str) -> str:
    """Extract the file extension from a URL or file path."""
    return os.path.splitext(url)[1].lower().lstrip(".")

def get_temp_file_path(filename: str = "input_file.bin") -> Path:
    """Return a Path object for a file inside the tempdata folder."""
    temp_dir = Path("tempdata")
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / filename
