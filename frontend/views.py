from dataclasses import dataclass
import streamlit as st
import pandas as pd

from data import sum_volume, cocktail_count, is_dev
from plots import generate_volume_treemap, generate_recipes_treemap


@dataclass
class DataFrameStats():
    countries: int
    machines: int
    recipes: int
    cocktails: int
    volume: int


def generate_sidebar(df: pd.DataFrame):
    """Generates the sidebar with the option. Returns needed variables"""
    st.sidebar.header("Filter CocktailBerry Data")
    st.sidebar.write("Here you can limit the data and filter a little bit.")
    st.sidebar.subheader("Filter Options")
    country_selection = sorted(list(df["Language"].unique()))
    countrycodes = st.sidebar.multiselect("Choose Countrycodes:", country_selection, country_selection)
    machine_selection = sorted(list(df["Machine Name"].unique()))
    machines = st.sidebar.multiselect("Choose Machines:", machine_selection, machine_selection)
    recipes_selection = sorted(list(df["Cocktailname"].unique()))
    recipes = st.sidebar.multiselect("Choose Recipes:", recipes_selection, recipes_selection)
    # also generates the needed data out of the df
    # since we got unique calculation already here (to save some compute things)
    df_stats = DataFrameStats(
        len(country_selection),
        len(machine_selection),
        len(recipes_selection),
        len(df),
        df["Volume"].sum() / 1000,
    )
    return countrycodes, machines, recipes, df_stats


def display_introduction(df_stats: DataFrameStats):
    st.title("🍹CocktailBerry Dashboard")
    st.markdown("Dashboard for all the [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) machines data!")
    with st.expander("What is this?"):
        __what_is_this()
    st.markdown(
        f"""
        # 📈 Current CocktailBerry Stats
        - 🍸 **{df_stats.cocktails}** cocktails made
        - 🎊 **{df_stats.volume:.1f}** litre cocktails produced
        - 🕹️ **{df_stats.machines}** machines sending data
        - 🌐 **{df_stats.countries}** languages used
        - 🧾 **{df_stats.recipes}** different recipes produced
        """
    )


def __what_is_this():
    st.markdown(
        """
        This is the official WebApp / Dashboard for the [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) project.
        If you don't know it, go check it out, it's super cool. 🚀

        In short, CocktailBerry is a Python software for the Rapsberry Pi
        to easily server cocktails and do lots of additional things for your party. The users can send their cocktail data
        (volume, cocktail name) with the according machine data (machine name, language settings) to an API endpoint. ⚙️

        This dashboard will then use the data and visualize it to give you some insights into the data.
        Have a look around on this page, visit the GitHub project, and if you are fond of the project, try it out or even leave a star. ⭐
        """
    )


def display_data(df: pd.DataFrame, filterd_df: pd.DataFrame):
    volume_df = sum_volume(filterd_df)
    recipe_df = cocktail_count(filterd_df)
    st.header("🍸 Volume and Number of Cocktails")
    generate_volume_treemap(volume_df)
    with st.expander("[Table] Aggregated by Language used and Machine Name:"):
        st.table(volume_df.style.format({"Cocktail Volume in Litre": "{:.2f}"}))

    st.header("🧾 Recipes Made")
    generate_recipes_treemap(recipe_df)
    with st.expander("[Table] Aggregated by Recipe Name and Language used:"):
        st.table(recipe_df)

    if is_dev:
        st.header("⚙️ Debug Stuff")
        with st.expander("All raw Data:"):
            st.table(df)


def display_footer():
    footer = """
    <div class="footer">
        <p class="left">Developed with ❤️</p>
        <p class="right">Data from <a href="https://github.com/AndreWohnsland/CocktailBerry">CocktailBerry</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
