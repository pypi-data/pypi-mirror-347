import requests
from .utils import replace_and_copy

def process_url(link):
    try:
        res = requests.get(link)
        res.raise_for_status()
        replace_and_copy(res.text)
    except Exception as e:
        print(f" Gagal membaca URL:\n{e}")
