import streamlit as st


def display_footer():
    """Generates the footer element with from HTML data"""
    footer = """
    <div class="footer">
        <p class="left">Made with ❤️</p>
        <p class="right">Data from <a href="https://github.com/AndreWohnsland/CocktailBerry">CocktailBerry</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
