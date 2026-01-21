from pathlib import Path

import streamlit as st

DIRPATH = Path(__file__).parent.absolute()
style_path = DIRPATH / "style.css"

# CSS to inject contained in a string
with style_path.open(encoding="utf-8") as f:
    STYLE_SETTINGS = f"<style>{f.read()}</style>"


def generate_style() -> None:
    """Style for Centered mode that app gets more width."""
    st.markdown(STYLE_SETTINGS, unsafe_allow_html=True)
