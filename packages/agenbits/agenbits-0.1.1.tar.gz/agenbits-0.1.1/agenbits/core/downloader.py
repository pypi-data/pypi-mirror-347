import requests

def fetch_data_from_url(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    raise Exception(f"Failed to fetch data. Status Code: {response.status_code}")
