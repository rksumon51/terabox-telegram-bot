import requests
import re

def get_download_link(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    html = r.text

    match = re.search(r'"downloadUrl":"(.*?)"', html)

    if match:
        link = match.group(1).replace("\\/", "/")
        return link
    else:
        raise Exception("Download link not found")
