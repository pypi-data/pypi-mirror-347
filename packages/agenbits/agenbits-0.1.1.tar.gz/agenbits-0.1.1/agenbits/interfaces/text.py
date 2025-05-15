import json
from agenbits.core.downloader import fetch_data_from_url
from agenbits.core.converter import save_binary_file
from agenbits.core.decoder import load_binary_file

def Text(path_or_url: str, type: str = "txt"):
    if path_or_url.startswith("http"):
        data = fetch_data_from_url(path_or_url)
        file_path = save_binary_file(data)
    else:
        file_path = path_or_url

    content = load_binary_file(file_path).decode("utf-8")

    if type == "json":
        return json.loads(content)
    elif type == "xml":
        return content  # Later: use xml.etree.ElementTree
    else:
        return content
