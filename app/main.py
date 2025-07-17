import os
import sys
import streamlit as st

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import the app
from ui.app import App

# Application entry point
if __name__ == "__main__":
    app = App()
    app.run()