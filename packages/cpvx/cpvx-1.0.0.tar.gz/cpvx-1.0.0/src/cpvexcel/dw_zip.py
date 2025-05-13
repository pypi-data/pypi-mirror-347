import requests
import zipfile
import io
import os
from .utils import get_data_dir

def download_and_extract_zip(link):
    try:
        res = requests.get(link)
        res.raise_for_status()

        data_folder = get_data_dir()
        os.makedirs(data_folder, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(res.content)) as zf:
            zf.extractall(data_folder)

        print(f"ZIP berhasil diekstrak ke folder '{data_folder}'")
    
    except Exception as e:
        print(f" Gagal download ZIP:\n{e}")
