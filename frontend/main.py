import streamlit as st

from data import generate_df, filter_dataframe
from styles import generate_style
import views


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
countrycodes, machines, recipes, recipes_limit, only_one_day, df_stats = views.generate_sidebar(df)
views.display_introduction(df_stats)

# skip this part if there is no data
if df.empty:
    st.info("Currently no data available. Let CocktailBerry send some data! ✨")
else:
    filtered_df = filter_dataframe(df, countrycodes, machines, recipes, only_one_day)
    views.display_data(filtered_df, recipes_limit, only_one_day)
views.display_api_instructions()
views.display_dev(df)
views.display_footer()
