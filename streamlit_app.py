import streamlit as st

from frontend.data import get_cocktails, filter_dataframe, get_installations
from frontend.styles import generate_style
from frontend import views


st.set_page_config(
    page_title="CocktailBerry Dashboard",
    page_icon="🍹",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://cocktailberry.readthedocs.io/",
        "Report a bug": "https://github.com/AndreWohnsland/CocktailBerry-WebApp/issues",
        "About": "# 🍹 CocktailBerry Dashboard \nDashboard for all the CocktailBerry machines data!",
    },
)
generate_style()

cocktails = get_cocktails()
installations = get_installations()
installation_count = len(installations)
country_codes, machines, recipes, recipes_limit, only_one_day, dates, df_stats = views.generate_sidebar(cocktails)
views.display_introduction(df_stats, installation_count)

# skip this part if there is no data
if cocktails.empty:
    st.info("Currently no data available. Let CocktailBerry send some data! ✨")
else:
    filtered_cocktails = filter_dataframe(cocktails, country_codes, machines, recipes, only_one_day, dates)  # type: ignore
    views.display_data(filtered_cocktails, recipes_limit, only_one_day)  # type: ignore
views.api_guidelines()
views.display_machine_types()
views.display_installations(installations)
views.display_dev(cocktails)
views.display_footer()
