import warnings
import pandas as pd
import plotly.express as px
import streamlit as st

from data import dfnames

# ignore the frame.append deprecation warning cause by plotly
warnings.filterwarnings("ignore")


def generate_volume_treemap(df: pd.DataFrame, country_split: bool = True):
    """Uses the language an machine name agg df to generate a treemap"""
    path = [px.Constant("Machines"), dfnames.machine_name]
    if country_split:
        path = [px.Constant("Language used"), dfnames.language, dfnames.machine_name]
    fig = px.treemap(df, path=path, values=dfnames.cocktail_volume, height=400)
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    fig.data[0].customdata = df[dfnames.cocktail_count].to_list()
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata} Cocktails<br>%{value:,.2f} l",
        hovertemplate='%{label}<br>Cocktail Volume: %{value:,.2f} l<br>Cocktails Made: %{customdata}<i>x</i>'
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def generate_recipes_treemap(df: pd.DataFrame, country_split: bool = True):
    """Uses the recipe agg df to generate a treemap"""
    path = [px.Constant("Recipes"), dfnames.cocktail_name]
    texttemplate = "<b>%{label}</b> <i>x</i>%{value:.0f}<br>"
    hovertemplate = '%{label}<br>Repice made: %{value:,.0f}<i>x</i>'
    if country_split:
        path = [px.Constant("Recipes"), dfnames.cocktail_name, dfnames.language]
        texttemplate = "<b>%{parent}</b> <i>x</i>%{value:.0f}<br>(%{label})"
        hovertemplate = '%{parent} (%{label})<br>Repice made: %{value:,.0f}<i>x</i>'
    fig = px.treemap(df, path=path, values=dfnames.cocktail_count, height=400)
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    fig.update_traces(
        texttemplate=texttemplate,
        hovertemplate=hovertemplate
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def generate_time_plot(df: pd.DataFrame):
    """Generates the cocktail count over the time"""
    fig = px.bar(
        df,
        x=dfnames.receivedate,
        y=dfnames.cocktail_count,
        color=dfnames.machine_name,
        barmode="group",
    )
    fig.update_layout(
        {"margin": {"l": 0, "r": 0, "t": 0, "b": 0}},
        bargroupgap=0,  # bargap=0,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_traces(marker_line_width=0, selector=dict(type="bar"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
