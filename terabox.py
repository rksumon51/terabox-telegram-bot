import requests
import re

def get_download_link(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise Exception("Failed to open TeraBox link")

    html = r.text

    # try to extract m3u8 or direct link
    match = re.search(r'https://[^"]+\.mp4', html)

    if match:
        return match.group(0)

    raise Exception("Download link not found")")
