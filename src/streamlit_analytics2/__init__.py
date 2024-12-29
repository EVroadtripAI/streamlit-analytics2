"""
Streamlit Analytics 2
Track & visualize user interactions with your streamlit app.
"""
from .state import data 
from .main import start_tracking, stop_tracking, track  # noqa: F401

__version__ = "0.9.1"
__name__ = "streamlit_analytics2"
