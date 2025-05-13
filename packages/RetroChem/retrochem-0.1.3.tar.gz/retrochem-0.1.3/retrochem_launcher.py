import sys
import streamlit.web.cli as stcli
import os

def main():
    script_path = os.path.join(os.path.dirname(__file__), "Scripts", "Retrochem.py")
    sys.argv = ["streamlit", "run", script_path]
    sys.exit(stcli.main())
