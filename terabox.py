import requests
import re

def get_download_link(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    html = r.text

    match = re.search(r'https://[^"]+\.mp4', html)

    if match:
        return match.group(0)
    else:
        raise Exception("Download link not found")
