import argparse
import os
from .pr_url import process_url
from .pr_path import process_path
from .dw_zip import download_and_extract_zip
from .tree_view import tree_view

def main():
    parser = argparse.ArgumentParser(description="PNXCL - Plugin Excel CLI")
    parser.add_argument("-v", "--version", action="version", version="cpv v1.0.0")
    parser.add_argument("--docs", action="store_true", help="Tampilkan lokasi dokumentasi")
    parser.add_argument("--lic", "--license", dest="license", action="store_true", help="Tampilkan lisensi")
    subparsers = parser.add_subparsers(dest="command")
    parser_pr = subparsers.add_parser("pr", help="Proses file .cpvxclrc dari URL atau path")
    parser_pr.add_argument("mode", choices=["url", "pth"], help="Mode input: 'url' atau 'pth'")
    parser_pr.add_argument("value", help="Link URL atau path file lokal")
    parser_dw = subparsers.add_parser("dw", help="Download dan ekstrak ZIP ke folder data/")
    parser_dw.add_argument("-url", required=True, help="Link langsung ke file ZIP (raw link)")
    subparsers.add_parser("tree", help="Tampilkan struktur folder")
    args = parser.parse_args()
    if args.docs:
        print("📚 Dokumentasi: https://pineplugins.github.io/cpvexcel/")
        return

    if args.license:
        try:
            with open(os.path.join(os.path.dirname(__file__), "LICENSE.txt"), encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ LICENSE.txt tidak ditemukan di package.")
        return

    match args.command:
        case "pr":
            process_url(args.value) if args.mode == "url" else process_path(args.value)
        case "dw":
            download_and_extract_zip(args.url)
        case "tree":
            tree_view()
