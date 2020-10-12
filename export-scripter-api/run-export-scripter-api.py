#!/usr/bin/env python3
import subprocess
import sys

def main():
    try:
        import scribus
        import importlib
        export_api = importlib.import_module("export-scripter-api")
        export_api.main()
    except ImportError:
        run_scribus()

def run_scribus() :
    call_args = ['scribus', '-g', '-py', sys.argv[0]]
    subprocess.call(call_args)

if __name__ == "__main__":
    main()
