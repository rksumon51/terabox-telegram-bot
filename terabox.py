import requests

def get_download_link(url):
    api = f"https://teraboxdownloader.nepcoderdevs.workers.dev/?url={url}"
    data = requests.get(api).json()

    if "download" in data:
        return data["download"]
    else:
        raise Exception("Download link not found")
