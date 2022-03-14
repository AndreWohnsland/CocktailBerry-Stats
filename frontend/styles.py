from pathlib import Path
import streamlit as st

DIRPATH = Path(__file__).parent.absolute()

# CSS to inject contained in a string
with open(DIRPATH / 'style.css', encoding="utf-8") as f:
    STYLESETTINGS = f"<style>{f.read()}</style>"


def generate_style():
    """Style for Centered mode that app gets more width"""
    st.markdown(STYLESETTINGS, unsafe_allow_html=True)
