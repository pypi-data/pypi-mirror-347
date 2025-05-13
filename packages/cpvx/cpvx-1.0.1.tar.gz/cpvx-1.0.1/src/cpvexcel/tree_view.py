import os
from .utils import get_data_dir

def tree_view(root_folder=None):
    if root_folder is None:
        root_folder = get_data_dir()

    if not os.path.exists(root_folder):
        print(f"Folder '{root_folder}' tidak ditemukan.")
        return

    for root, dirs, files in os.walk(root_folder):
        level = root.replace(root_folder, '').count(os.sep)
        indent = '│   ' * level + '├── ' if level else ''
        print(f"{indent}{os.path.basename(root)}/")
        for f in files:
            print(f"{'│   ' * (level + 1)}└── {f}")
