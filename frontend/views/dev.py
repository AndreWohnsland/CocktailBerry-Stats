import pandas as pd
import streamlit as st

from ..data import is_dev


def display_dev(df: pd.DataFrame) -> None:
    """Show dev thingies if devmode is on."""
    if is_dev:
        st.header("⚙️ Debug Stuff")
        q_params = st.query_params.to_dict()
        st.write(q_params)
        with st.expander("All raw Data:"):
            st.table(df)
