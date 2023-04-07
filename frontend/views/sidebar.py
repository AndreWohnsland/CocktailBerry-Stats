from datetime import datetime

import streamlit as st
import pandas as pd

from ..models import DataFrameStats, CocktailSchema


def generate_sidebar(df: pd.DataFrame):
    """Generates the sidebar with the option. Returns needed variables"""
    st.sidebar.subheader("🔍 Filter CocktailBerry Data")
    st.sidebar.write("Here you can limit the data and filter a little bit.")
    if df.empty:
        st.sidebar.write("Nothing to do, need some data ...")
        return [], [], [], 1, False, (None, None), DataFrameStats(0, 0, 0, 0, 0, "No Data", "No Data")
    st.sidebar.subheader("Filter Options")
    st.sidebar.caption("For your Party")
    only_one_day = st.sidebar.checkbox("Only Show last 24h Data", _get_partymode())
    st.sidebar.caption("Basic Settings")
    country_selection = sorted(list(df[CocktailSchema.language].unique()))
    country_codes = st.sidebar.multiselect("Choose Used Languages:", country_selection, country_selection)
    machine_selection = sorted(list(df[CocktailSchema.machine_name].unique()))
    machines = st.sidebar.multiselect("Choose Machines:", machine_selection, machine_selection)
    recipes_selection = sorted(list(df[CocktailSchema.cocktail_name].unique()))
    recipes_limit = st.sidebar.slider(
        "Show x most Popular Recipes:", 2, max(2, len(recipes_selection)), min(10, len(recipes_selection))
    )
    min_date = datetime.date(min(df[CocktailSchema.receivedate]))
    max_date = datetime.date(max(df[CocktailSchema.receivedate]))
    with st.sidebar.expander("Advanced Settings"):
        start_date = st.date_input("Start Date", value=min_date)
        end_date = st.date_input("End Date", value=max_date)
        dates = (start_date, end_date)
        recipes = st.multiselect("Choose Recipes:", recipes_selection, recipes_selection)
    # also generates the needed data out of the df
    # since we got unique calculation already here (to save some compute things)
    df_stats = DataFrameStats(
        len(country_selection),
        len(machine_selection),
        len(recipes_selection),
        len(df),
        df[CocktailSchema.volume].sum() / 1000,
        _build_date(df[CocktailSchema.receivedate].min()),
        _build_date(df[CocktailSchema.receivedate].max()),
    )
    return country_codes, machines, recipes, recipes_limit, only_one_day, dates, df_stats


def _get_partymode() -> bool:
    """Returns if the query requested only data of today"""
    q_params = st.experimental_get_query_params()
    partymode = q_params.get("partymode")
    use_party = partymode is not None and partymode[0].lower() == "true"
    return use_party


def _build_date(checkdate: datetime) -> str:
    yyyymmddfmt = "%a, %d. %b %Y"
    if checkdate.date() == datetime.today().date():
        return "today"
    return checkdate.strftime(yyyymmddfmt)
