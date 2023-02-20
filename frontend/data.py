import os
import datetime
import json
import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
is_dev = os.getenv("DEBUG") is not None
backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
DATEFORMAT_STR = "%d/%m/%Y, %H:%M"


class DataSchema():
    machine_name: str = "Machine Name"
    cocktail_name: str = "Cocktail Name"
    cocktail_count: str = "Number of Cocktails"
    cocktail_volume: str = "Cocktail Volume in Litre"
    volume: str = "Volume"
    language: str = "Language"
    receivedate: str = "Received Date"


class ReceivedData():
    COUNTRYCODE = "countrycode"
    MACHINENAME = "machinename"
    COCKTAILNAME = "cocktailname"
    VOLUME = "volume"
    RECEIVEDATE = "receivedate"


# DataSchema = DataSchema()


def __myround(x, base=5):
    """Rounds to the nearest number to given base"""
    return base * round(x / base)


@st.cache_data(ttl=60)
def generate_df():
    """Gets the data from deta and converts to df"""
    cocktails_response = requests.get(f"{backend_url}/public/cocktails", timeout=10)
    cocktails = {}
    if cocktails_response.ok:
        cocktails = json.loads(cocktails_response.text)
    df = pd.DataFrame(cocktails).rename(columns={
        ReceivedData.COUNTRYCODE: DataSchema.language,
        ReceivedData.MACHINENAME: DataSchema.machine_name,
        ReceivedData.COCKTAILNAME: DataSchema.cocktail_name,
        ReceivedData.VOLUME: DataSchema.volume,
        ReceivedData.RECEIVEDATE: DataSchema.receivedate,
    })
    if not df.empty:
        df = df[[
            DataSchema.language,
            DataSchema.machine_name,
            DataSchema.cocktail_name,
            DataSchema.volume,
            DataSchema.receivedate,
        ]]
        df[DataSchema.receivedate] = pd.to_datetime(df[DataSchema.receivedate], format=DATEFORMAT_STR)
    return df


@st.cache_data(ttl=60)
def filter_dataframe(df: pd.DataFrame, countries: list, machines: list, recipes: list, only_one_day: bool):
    """Applies the sidebar filter option to the data"""
    filtered_df = df.loc[
        df[DataSchema.language].isin(countries) &
        df[DataSchema.machine_name].isin(machines) &
        df[DataSchema.cocktail_name].isin(recipes)
    ]
    if only_one_day:
        filtering = filtered_df[DataSchema.receivedate] >= (
            datetime.datetime.now() - datetime.timedelta(hours=24))  # type: ignore
        filtered_df = filtered_df[filtering]
    return filtered_df


@st.cache_data(ttl=60)
def sum_volume(df: pd.DataFrame, country_split: bool) -> pd.DataFrame:
    """Aggregate by language and machine Name, returns total volumes and cocktail counts"""
    grouping = [DataSchema.machine_name]
    if country_split:
        grouping = [DataSchema.language, DataSchema.machine_name]
    volumes = (
        df.groupby(grouping)[DataSchema.volume]   # type: ignore
        .agg(["sum", "count"]).reset_index()
        .sort_values(['sum', 'count'], ascending=False)
        .rename(columns={
            "sum": DataSchema.cocktail_volume,
            "count": DataSchema.cocktail_count,
        }))
    volumes[DataSchema.cocktail_volume] = volumes[DataSchema.cocktail_volume] / 1000
    return volumes


@st.cache_data(ttl=60)
def cocktail_count(df: pd.DataFrame, limit_recipe: int, country_split: bool) -> pd.DataFrame:
    """Aggregate by language and cocktail name, limits to x most used recipes"""
    grouping = [DataSchema.cocktail_name]
    if country_split:
        grouping = [DataSchema.cocktail_name, DataSchema.language]
    # first group by the restrictions, this needs to be done in both cases
    cocktails = (
        df.groupby(grouping)[DataSchema.volume]  # type: ignore
        .count()
        .reset_index()
        .rename(columns={DataSchema.volume: DataSchema.cocktail_count, })
    )
    # if no split, the logic is quite simple, just sort and limit them
    if not country_split:
        cocktails.sort_values([DataSchema.cocktail_count], ascending=False, inplace=True)
        cocktails = cocktails.iloc[:limit_recipe]
        return cocktails
    # If split by country, for the listing, we need to generate a tmp rank
    # that we can order by that rank for the cocktail name (its dependant on total count)
    name_order = (
        df.groupby([DataSchema.cocktail_name])[DataSchema.volume]
        .count()
        .sort_values()
        .index
        .to_list()[-limit_recipe:]
    )
    sorter_index = dict(zip(name_order, range(len(name_order))))
    cocktails['Rank'] = cocktails[DataSchema.cocktail_name].map(sorter_index)
    cocktails.sort_values(['Rank', DataSchema.cocktail_count], ascending=False, inplace=True)
    cocktails.dropna(axis=0, inplace=True)
    cocktails.drop('Rank', 1, inplace=True)
    return cocktails


@st.cache_data(ttl=60)
def time_aggregation(df: pd.DataFrame, hour_grouping: bool, machine_grouping: bool) -> pd.DataFrame:
    """Aggregates the data either by day or hour, depending on the last_day param"""
    freq = "1D"
    if hour_grouping:
        freq = "1h"
    date_grouper = pd.Grouper(key=DataSchema.receivedate, freq=freq)
    grouping = [date_grouper]
    if machine_grouping:
        grouping = [date_grouper, DataSchema.machine_name]
    time_df = (
        df.groupby(grouping)[DataSchema.cocktail_name]  # type: ignore
        .count()
        .reset_index()
        .rename(columns={DataSchema.cocktail_name: DataSchema.cocktail_count, })
    )
    time_df = time_df[time_df[DataSchema.cocktail_count] != 0]
    return time_df


@st.cache_data(ttl=60)
def serving_aggregation(df: pd.DataFrame, machine_split: bool, min_count: int):
    """Aggregates by serving sizes"""
    # rounds to the closest 25
    serving_df = df.copy(deep=True)
    serving_df[DataSchema.volume] = serving_df[DataSchema.volume].apply(__myround, args=(25,))
    grouping = [DataSchema.volume]
    if machine_split:
        grouping = [DataSchema.machine_name, DataSchema.volume]
    serving_df = (
        serving_df.groupby(grouping)[DataSchema.language]  # type: ignore
        .agg(["count"])
        .reset_index()
        .sort_values([DataSchema.volume], ascending=True)
        .rename(columns={"count": DataSchema.cocktail_count, })
    )
    # for multiple grouping needs to calculate the sum per group and only include the ones having more than min
    serving_size_count = serving_df.groupby(DataSchema.volume).sum()
    volumes_to_keep = serving_size_count[serving_size_count[DataSchema.cocktail_count] >= min_count].index.to_list()
    return serving_df[serving_df[DataSchema.volume].isin(volumes_to_keep)]
