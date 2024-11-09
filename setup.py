import importlib
import subprocess
import sys
import requests
import os
import zipfile
from tqdm import tqdm


def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = importlib.import_module(package)


def download_file(url, filename):
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        total_size = int(response.headers.get('content-length', 0))
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
            for chunk in response.iter_content(1024):
                f.write(chunk)
                pbar.update(len(chunk))


def unzip_file(zip_path, extract_to):
    print(f"Unzipping {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc='Extracting '):
            try:
                zip_ref.extract(member, extract_to)
            except zipfile.error as e:
                print(f"Error extracting {member}: {e}")


def main():
    packages = ["requests", "tqdm", "beautifulsoup4", "numpy"]
    for package in packages:
        install_and_import(package)

    url1 = "https://library.ldraw.org/library/updates/complete.zip"
    url2 = "https://github.com/TobyLobster/ImportLDraw/releases/download/v1.2.0/importldraw1.2.0.zip"

    download_file(url1, 'complete.zip')
    download_file(url2, 'importldraw.zip')

    unzip_file('complete.zip', os.path.abspath("complete"))
    unzip_file('importldraw.zip', os.path.abspath("importldraw"))


if __name__ == "__main__":
    main()
