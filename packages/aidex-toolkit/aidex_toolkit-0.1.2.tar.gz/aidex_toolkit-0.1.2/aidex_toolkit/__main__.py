# aidex_toolkit/__main__.py
import sys
from aidex_toolkit import __version__

def main():
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"aidex_toolkit version {__version__}")
    else:
        print("Welcome to aidex_toolkit! Use --version to check the version.")
