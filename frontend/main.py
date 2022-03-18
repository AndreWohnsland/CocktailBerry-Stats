import streamlit as st

from data import generate_df, filter_dataframe
from styles import generate_style
from views import display_data, display_introduction, generate_sidebar, display_footer, display_api_instructions, display_dev


st.set_page_config(
    page_title="CocktailBerry Dashboard",
    page_icon="🍹",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/AndreWohnsland/CocktailBerry',
        'Report a bug': "https://github.com/AndreWohnsland/CocktailBerry-WebApp/issues",
        'About': "# 🍹 CocktailBerry Dashboard \nDashboard for all the CocktailBerry machines data!"
    }
)
generate_style()

df = generate_df()
countrycodes, machines, recipes, recipes_limit, only_one_day, df_stats = generate_sidebar(df)
display_introduction(df_stats)

# skip this part if there is no data
if df.empty:
    st.write("Currently no data available. Let CocktailBerry send some data! 🥺")
else:
    filtered_df = filter_dataframe(df, countrycodes, machines, recipes, only_one_day)
    display_data(filtered_df, recipes_limit, only_one_day)
display_api_instructions()
display_dev(df)
display_footer()
