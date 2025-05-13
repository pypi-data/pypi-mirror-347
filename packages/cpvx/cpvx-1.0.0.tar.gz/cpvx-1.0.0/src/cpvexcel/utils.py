import pyperclip
import os

def get_base_dir():
    # Ambil folder "cpvexcel", lokasi file ini berada
    return os.path.dirname(os.path.abspath(__file__))

def get_data_dir():
    return os.path.join(get_base_dir(), 'data')

def replace_and_copy(content):
    processed = content.replace("<t>", "\t")
    pyperclip.copy(processed)
    print("Nilai berhasil disalin ke clipboard.")
