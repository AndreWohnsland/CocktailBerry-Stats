import streamlit as st

from data import generate_df, filter_dataframe
from styles import generate_style
from views import display_data, display_introduction, generate_sidebar, display_footer


st.set_page_config(
    page_title="CocktailBerry Dashboard",
    page_icon="🍹",
    initial_sidebar_state="collapsed"
)
generate_style()

df = generate_df()
countrycodes, machines, recipes, df_stats = generate_sidebar(df)
filtered_df = filter_dataframe(df, countrycodes, machines, recipes)

display_introduction(df_stats)
display_data(df, filtered_df)
display_footer()
