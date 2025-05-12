import argparse
import sys
import subprocess
from .transpiler import translate
from .__version__ import __version__

def run_file(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            farsi_code = f.read()
        translated = translate(farsi_code)
        exec(translated, {})
    except Exception as e:
        print("Error executing code:", e)

def main():
    parser = argparse.ArgumentParser(description="FarsiLang: Persian programming language based on Python")
    parser.add_argument("file", nargs="?", help="file destination.farsi")
    parser.add_argument("-v", "--version", action="store_true", help="show version")

    args = parser.parse_args()

    if args.version:
        print("FarsiLang Versiom", __version__)
    elif args.file:
        run_file(args.file) # , debug=args.debug
    else:
        parser.print_help()
