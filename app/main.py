import os
import sys
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

repo_root = os.path.dirname(os.path.abspath(__file__))  # /mount/src/ai-recruitment-platform/app
repo_root = os.path.dirname(repo_root)  # /mount/src/ai-recruitment-platform
sys.path.insert(0, repo_root)

# Now import the app
from app.ui.app import App

# Application entry point
if __name__ == "__main__":
    app = App()
    app.run()