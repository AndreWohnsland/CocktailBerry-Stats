import os
import streamlit as st
from deta import Deta
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
isDev = os.getenv("DEBUG") is not None
TABLE_NAME = "cocktails" + ("_dev" if isDev else "")
deta = Deta(os.getenv("DETA_BASE_KEY"))
cocktail_deta = deta.Base(TABLE_NAME)


@st.cache(ttl=60)
def generate_df():
    cocktails = cocktail_deta.fetch().items
    df = pd.DataFrame(cocktails).rename(columns={
        "countrycode": "Countrycode",
        "machinename": "Machinename",
        "cocktailname": "Cocktailname",
        "volume": "Volume",
    })
    df.drop("key", axis=1, inplace=True)
    return df


@st.cache(ttl=60)
def sum_volume(df: pd.DataFrame) -> pd.DataFrame:
    volumes = df.groupby(["Countrycode", "Machinename"])["Volume"] \
        .agg(["sum", "count"]).reset_index() \
        .sort_values(['sum', 'count'], ascending=False) \
        .rename(columns={
            "sum": "Cocktail Volume in ml",
            "count": "Number of Cocktails",
        })
    return volumes


@st.cache(ttl=60)
def cocktail_count(df: pd.DataFrame) -> pd.DataFrame:
    cocktails = df.groupby(["Cocktailname", "Countrycode"])["Volume"] \
        .count().reset_index() \
        .rename(columns={
            "Volume": "Number of Cocktails",
        })
    return cocktails
