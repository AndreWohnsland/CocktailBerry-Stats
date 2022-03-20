import os
import datetime
from dataclasses import dataclass
import streamlit as st
from deta import Deta
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
is_dev = os.getenv("DEBUG") is not None
TABLE_NAME = "cocktails" + ("_dev" if is_dev else "")
deta = Deta(os.getenv("DETA_BASE_KEY"))
cocktail_deta = deta.Base(TABLE_NAME)
DATEFORMAT_STR = "%d/%m/%Y, %H:%M"


@dataclass
class DfNames():
    machine_name: str = "Machine Name"
    cocktail_name: str = "Cocktail Name"
    cocktail_count: str = "Number of Cocktails"
    cocktail_volume: str = "Cocktail Volume in Litre"
    volume: str = "Volume"
    language: str = "Language"
    receivedate: str = "Received Date"


dfnames = DfNames()


@st.cache(ttl=60)
def generate_df():
    """Gets the data from deta and converts to df"""
    cocktails = cocktail_deta.fetch().items
    df = pd.DataFrame(cocktails).rename(columns={
        "countrycode": dfnames.language,
        "machinename": dfnames.machine_name,
        "cocktailname": dfnames.cocktail_name,
        "volume": dfnames.volume,
        "receivedate": dfnames.receivedate,
    })
    if not df.empty:
        df = df[[
            dfnames.language,
            dfnames.machine_name,
            dfnames.cocktail_name,
            dfnames.volume,
            dfnames.receivedate,
        ]]
        df[dfnames.receivedate] = pd.to_datetime(df[dfnames.receivedate], format=DATEFORMAT_STR)
    return df


@st.cache(ttl=60)
def filter_dataframe(df: pd.DataFrame, countries: list, machines: list, recipes: list, only_one_day: bool):
    """Applies the sidebar filter option to the data"""
    filtered_df = df.loc[
        df[dfnames.language].isin(countries) &
        df[dfnames.machine_name].isin(machines) &
        df[dfnames.cocktail_name].isin(recipes)
    ]
    if only_one_day:
        filtering = filtered_df[dfnames.receivedate] >= (datetime.datetime.now() - datetime.timedelta(hours=24))
        filtered_df = filtered_df[filtering]
    return filtered_df


@st.cache(ttl=60)
def sum_volume(df: pd.DataFrame, country_split: bool) -> pd.DataFrame:
    """Aggregate by language and machine Name, returns total volumes and cocktail counts"""
    grouping = [dfnames.machine_name]
    if country_split:
        grouping = [dfnames.language, dfnames.machine_name]
    volumes = df.groupby(grouping)[dfnames.volume] \
        .agg(["sum", "count"]).reset_index() \
        .sort_values(['sum', 'count'], ascending=False) \
        .rename(columns={
            "sum": dfnames.cocktail_volume,
            "count": dfnames.cocktail_count,
        })
    volumes[dfnames.cocktail_volume] = volumes[dfnames.cocktail_volume] / 1000
    return volumes


@st.cache(ttl=60)
def cocktail_count(df: pd.DataFrame, limit_recipe: int, country_split: bool) -> pd.DataFrame:
    """Aggregate by language and cocktailname, limits to x most used recipes"""
    grouping = [dfnames.cocktail_name]
    if country_split:
        grouping = [dfnames.cocktail_name, dfnames.language]
    # first group by the restrictions, this needs to be done in both cases
    cocktails = df.groupby(grouping)[dfnames.volume] \
        .count().reset_index().rename(columns={
            dfnames.volume: dfnames.cocktail_count,
        })
    # if no split, the logic is quite simple, just sort and limit them
    if not country_split:
        cocktails.sort_values([dfnames.cocktail_count], ascending=False, inplace=True)
        cocktails = cocktails.iloc[:limit_recipe]
        return cocktails
    # If split by country, for the listing, we need to generate a tmp rank
    # that we can order by that rank for the cocktail name (its dependant on total count)
    nameorder = df.groupby([dfnames.cocktail_name])[dfnames.volume].count() \
        .sort_values().index.to_list()[-limit_recipe:]
    sorter_index = dict(zip(nameorder, range(len(nameorder))))
    cocktails['Rank'] = cocktails[dfnames.cocktail_name].map(sorter_index)
    cocktails.sort_values(['Rank', dfnames.cocktail_count], ascending=False, inplace=True)
    cocktails.dropna(axis=0, inplace=True)
    cocktails.drop('Rank', 1, inplace=True)
    return cocktails


@st.cache(ttl=60)
def time_aggregation(df: pd.DataFrame, hour_grouping: bool, machine_grouping: bool) -> pd.DataFrame:
    """Aggregates the data either by day or hour, depending on the last_day param"""
    freq = "1D"
    if hour_grouping:
        freq = "1h"
    date_grouper = pd.Grouper(key=dfnames.receivedate, freq=freq)
    grouping = [date_grouper]
    if machine_grouping:
        grouping = [date_grouper, dfnames.machine_name]
    time_df = df.groupby(grouping)[dfnames.cocktail_name].count().reset_index().rename(
        columns={dfnames.cocktail_name: dfnames.cocktail_count, }
    )
    return time_df
