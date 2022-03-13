import streamlit as st

# CSS to inject contained in a string
STYLESETTINGS = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            .appview-container .main .block-container{
                padding-top: 1rem;
                max-width: 1000px;
            }
            </style>
            """


def generate_style():
    """Style for Centered mode that app gets more width"""
    st.markdown(STYLESETTINGS, unsafe_allow_html=True)
