import streamlit as st

from ..data import is_dev


def display_dev(df):
    """show dev thingies if devmode is on"""
    if is_dev:
        st.header("⚙️ Debug Stuff")
        q_params = st.experimental_get_query_params()
        st.write(q_params)
        with st.expander("All raw Data:"):
            st.table(df)
