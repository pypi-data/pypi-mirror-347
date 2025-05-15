import mimetypes

def detect_file_type_from_url(url: str) -> str:
    type_guess, _ = mimetypes.guess_type(url)
    if type_guess:
        return type_guess
    return "application/octet-stream"
