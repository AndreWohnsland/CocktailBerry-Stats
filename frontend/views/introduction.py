import streamlit as st

from ..models import DataFrameStats


def display_introduction(df_stats: DataFrameStats, installations: int) -> None:
    """Display some basic information and stats about the data & project."""
    st.header("🍹CocktailBerry Dashboard")
    st.markdown("Dashboard for all the [CocktailBerry](https://cocktailberry.readthedocs.io/) machines data!")
    with st.expander("What is this?"):
        _what_is_this()
    st.markdown(
        f"""
        ## 📈 Current CocktailBerry Stats
        - 🍸 **{df_stats.cocktails}** cocktails made
        - 🧾 **{df_stats.recipes}** different recipes tasted
        - 🎊 **{df_stats.volume:.1f}** litre cocktails produced
        - 🕹️ **{df_stats.machines}** machines sending data
        - 📦 **{installations}** installations registered
        - 🌐 **{df_stats.countries}** languages used
        - 🧊 oldest data: **{df_stats.first_data}**
        - 🔥 latest data: **{df_stats.last_data}**
        """
    )


def _what_is_this() -> None:
    """Return some additional information about the dashboard."""
    st.markdown(
        """
        This is the official WebApp / Dashboard for the [CocktailBerry](https://cocktailberry.readthedocs.io/) project.
        If you don't know it, go check it out, it's super cool. 🚀

        In short, CocktailBerry is a Python software for the Raspberry Pi
        to easily server cocktails and do lots of additional things for your party.
        The users can send their cocktail data (volume, cocktail name)
        with the according machine data (machine name, language settings) to an API endpoint. ⚙️

        This dashboard will then use the data and visualize it to give you some insights into the data.
        Have a look around on this page, visit the GitHub project,
        and if you are fond of the project, try it out or even leave a star. ⭐
        """
    )
