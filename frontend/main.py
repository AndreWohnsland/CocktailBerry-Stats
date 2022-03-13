import streamlit as st

from utils import generate_sidebar
from aggregations import generate_df, sum_volume, cocktail_count
from plots import generate_volume_treemap
from styles import hide_table_row_index


st.set_page_config(
    page_title="CocktailBerry Dashboard",
    page_icon="🍹",
)

countrycodes = generate_sidebar()
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.title("🍹CocktailBerry Dashboard")
st.write("Dashboard for all the CocktailBerry Machines Data!")

df = generate_df()
volume_df = sum_volume(df)
recipe_df = cocktail_count(df)

st.table(df)

st.header("Volume and Number of Cocktails")
st.write("Aggregated by Countrycode and Machinename")
st.table(volume_df)
generate_volume_treemap(volume_df)

st.header("Recipes Made")
st.write("Aggregated by Recipe Name and Countrycode")
st.table(recipe_df)
