def Binary(path_or_url: str):
    # Just fetch and save binary; return path for user to handle
    from agenbits.core.downloader import fetch_data_from_url
    from agenbits.core.converter import save_binary_file

    if path_or_url.startswith("http"):
        raw_data = fetch_data_from_url(path_or_url)
        binary_path = save_binary_file(raw_data, filename="binary_input.bin")
    else:
        with open(path_or_url, "rb") as f:
            raw_data = f.read()
        binary_path = save_binary_file(raw_data, filename="binary_input.bin")

    return binary_path
