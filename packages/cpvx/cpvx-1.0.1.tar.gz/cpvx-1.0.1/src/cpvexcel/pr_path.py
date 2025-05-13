import os
from .utils import get_base_dir, replace_and_copy

def process_path(path):
    try:
        if not os.path.isabs(path):
            path = os.path.join(get_base_dir(), path)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        replace_and_copy(content)
    except Exception as e:
        print(f" Gagal membaca file lokal:\n{e}")
