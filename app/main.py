import os
import sys
import streamlit as st

from dotenv import load_dotenv
load_dotenv()


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now import the app
from app.ui.app import App

# Application entry point
if __name__ == "__main__":
    app = App()
    app.run()