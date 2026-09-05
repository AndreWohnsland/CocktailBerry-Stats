import pandas as pd
import streamlit as st

from ..environment import SETTINGS


def display_dev(df: pd.DataFrame) -> None:
    """Show dev thingies if devmode is on."""
    if SETTINGS.debug:
        st.header("⚙️ Debug Stuff")
        q_params = st.query_params.to_dict()
        st.write(q_params)
        with st.expander("All raw Data:"):
            st.table(df)
