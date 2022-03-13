import streamlit as st

from utils import generate_sidebar
from aggregations import generate_df, sum_volume, cocktail_count
from plots import generate_volume_treemap, generate_recipes_treemap
from styles import generate_style


st.set_page_config(
    page_title="CocktailBerry Dashboard",
    page_icon="🍹",
)

countrycodes = generate_sidebar()
generate_style()

st.title("🍹CocktailBerry Dashboard")
st.write("Dashboard for all the CocktailBerry Machines Data!")

df = generate_df()
volume_df = sum_volume(df)
recipe_df = cocktail_count(df)

st.header("Volume and Number of Cocktails")
with st.expander("Aggregated by Countrycode and Machinename (Table):"):
    st.table(volume_df)
generate_volume_treemap(volume_df)

st.header("Recipes Made")
with st.expander("Aggregated by Recipe Name and Countrycode (Table):"):
    st.table(recipe_df)
generate_recipes_treemap(recipe_df)


st.header("Debug Stuff")
with st.expander("All raw Data:"):
    st.table(df)
