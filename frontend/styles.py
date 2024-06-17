from pathlib import Path

import streamlit as st

DIRPATH = Path(__file__).parent.absolute()

# CSS to inject contained in a string
with open(DIRPATH / 'style.css', encoding="utf-8") as f:
    STYLE_SETTINGS = f"<style>{f.read()}</style>"


def generate_style():
    """Style for Centered mode that app gets more width."""
    st.markdown(STYLE_SETTINGS, unsafe_allow_html=True)
