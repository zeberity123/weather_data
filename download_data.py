import os
import requests
from tqdm import tqdm

with open('urls.txt') as f:
    lines = f.readlines()
    urls = [line.strip() for line in lines]

TOKEN = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImJpcnRoMDUwOCIsImV4cCI6MTczNjU1NDE5NywiaWF0IjoxNzMxMzcwMTk3LCJpc3MiOiJodHRwczovL3Vycy5lYXJ0aGRhdGEubmFzYS5nb3YifQ.QxtQ6LhuV6_GeyWlFmS6RIsFVAUQwrsc5O0MjI2xYUoh69Wl8moq9wyMMuSlKmsSrOPO82c24NjjBSKhdDOnOTVLgsGUD49fUcpnJqeDixnQTn7jQVqv0dXNk7CXPY5L3ftmg7pLbmjfxkZOB_8U9jF-rk-AX-gCuYodZGG4AZnZo_WX1ZI46yuk-fN2AiVzhOBSgEUPHPxFpoRA4IFy0oMCT9gu4-75wbwW8OQUkmY5pvjqgYcRFhAGSLmFIgxhqbk9cU7FvGRqy1Ry3G8A1v2MLDaXe4eydwIKv9qLroGzN4oKhxiVMtPQseZUT5GtxvAAOMpiJ2vbOSHZQfxnng"

if not TOKEN:
    raise EnvironmentError("Please set the EARTHDATA_TOKEN environment variable with your access token.")

DOWNLOAD_DIR = 'downloaded_hdf5'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_file(url, session, headers):
    local_filename = os.path.join(DOWNLOAD_DIR, url.split('/')[-1])

    if os.path.exists(local_filename):
        print(f"File already exists: {local_filename}. Skipping download.")
        return

    with session.get(url, headers=headers, stream=True) as response:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred while downloading {url}: {err}")
            return

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024

        progress = tqdm(total=total_size, unit='iB', unit_scale=True, desc=local_filename)

        with open(local_filename, 'wb') as file:
            for data in response.iter_content(block_size):
                if data:
                    progress.update(len(data))
                    file.write(data)
        progress.close()

        if total_size != 0 and progress.n != total_size:
            print(f"WARNING: Downloaded size for {local_filename} does not match expected size.")
        else:
            print(f"Successfully downloaded: {local_filename}")

def main():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0 (compatible; EarthdataDownloader/1.0)'
    }

    with requests.Session() as session:
        for url in urls:
            print(f"Starting download: {url}")
            download_file(url, session, headers)

if __name__ == "__main__":
    main()