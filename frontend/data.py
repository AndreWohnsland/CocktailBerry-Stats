import os
import streamlit as st
from deta import Deta
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
is_dev = os.getenv("DEBUG") is not None
TABLE_NAME = "cocktails" + ("_dev" if is_dev else "")
deta = Deta(os.getenv("DETA_BASE_KEY"))
cocktail_deta = deta.Base(TABLE_NAME)


@st.cache(ttl=60)
def generate_df():
    """Gets the data from deta and converts to df"""
    cocktails = cocktail_deta.fetch().items
    df = pd.DataFrame(cocktails).rename(columns={
        "countrycode": "Language",
        "machinename": "Machine Name",
        "cocktailname": "Cocktailname",
        "volume": "Volume",
    })
    if not df.empty:
        df.drop(["key", "keyname"], axis=1, inplace=True)
    return df


@st.cache(ttl=60)
def filter_dataframe(df: pd.DataFrame, countries: list, machines: list, recipes: list):
    """Applies the sidebar filter option to the data"""
    filtered_df = df.loc[
        df["Language"].isin(countries) &
        df["Machine Name"].isin(machines) &
        df["Cocktailname"].isin(recipes)
    ]
    return filtered_df


@st.cache(ttl=60)
def sum_volume(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate by language and machine Name, returns total volumes and cocktail counts"""
    volumes = df.groupby(["Language", "Machine Name"])["Volume"] \
        .agg(["sum", "count"]).reset_index() \
        .sort_values(['sum', 'count'], ascending=False) \
        .rename(columns={
            "sum": "Cocktail Volume in Litre",
            "count": "Number of Cocktails",
        })
    volumes["Cocktail Volume in Litre"] = volumes["Cocktail Volume in Litre"] / 1000
    return volumes


@st.cache(ttl=60)
def cocktail_count(df: pd.DataFrame, limit_recipe: int = 10) -> pd.DataFrame:
    """Aggregate by language and cocktailname, limits to x most used recipes"""
    nameorder = df.groupby(["Cocktailname"])["Volume"].count().sort_values().index.to_list()[-limit_recipe:]
    sorter_index = dict(zip(nameorder, range(len(nameorder))))
    cocktails = df.groupby(["Cocktailname", "Language"])["Volume"] \
        .count().reset_index() \
        .rename(columns={
            "Volume": "Number of Cocktails",
        })
    cocktails['Rank'] = cocktails['Cocktailname'].map(sorter_index)
    cocktails.sort_values(['Rank', 'Number of Cocktails'], ascending=False, inplace=True)
    cocktails.dropna(axis=0, inplace=True)
    cocktails.drop('Rank', 1, inplace=True)
    return cocktails
