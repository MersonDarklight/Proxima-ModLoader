import requests
import os
import sys
from time import sleep

def get_latest_release(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_asset(asset_url, filename, output_dir, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    headers['Accept'] = 'application/octet-stream'

    response = requests.get(asset_url, headers=headers, stream=True)
    response.raise_for_status()

    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Загружено: {filename}.")

def main():
    try:
        release = get_latest_release("MersonDarklight", "Proxima-ModLoader")
        print(f"Загружается релиз {release['tag_name']}...")

        for asset in release.get('assets', []):
            print(f"Загрузка файла {asset['name']}...")
            download_asset(asset['url'], asset['name'], "./", None)

    except requests.RequestException as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
    sleep(5)
    os.execv(sys.executable, ['python', 'pmodloader.py'])