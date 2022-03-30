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
    fig = px.treemap(df, path=path, values=dfnames.cocktail_volume, height=400, hover_data=[dfnames.cocktail_count])
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata} Cocktails<br>%{value:,.2f} l",
        hovertemplate='%{label}<br>Cocktails Made: %{customdata}<i>x</i><br>Cocktail Volume: %{value:,.2f} l'
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


def generate_time_plot(df: pd.DataFrame, machine_grouping: bool):
    """Generates the cocktail count over the time"""
    aditional_params = {}
    if machine_grouping:
        aditional_params["color"] = dfnames.machine_name
    fig = px.bar(
        df,
        x=dfnames.receivedate,
        y=dfnames.cocktail_count,
        barmode="group",
        ** aditional_params,
    )
    fig.update_layout(
        {"margin": {"l": 0, "r": 0, "t": 0, "b": 0}},
        bargroupgap=0,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis_title=None,
    )
    fig.update_traces(marker_line_width=0, selector=dict(type="bar"))
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(step="all")
            ]),
            activecolor="#ff0000",
            font=dict(color="#000000"),
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.01
        )
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def generate_serving_size_bars(df: pd.DataFrame):
    """Crerates a bar chart with the serving sizes"""
    fig = px.bar(
        df,
        x=dfnames.volume,
        y=dfnames.cocktail_count,
    )
    fig.update_layout(
        {"margin": {"l": 0, "r": 0, "t": 0, "b": 0}},
        bargroupgap=0,
        xaxis_title=None,
    )
    fig.update_traces(marker_line_width=0, selector=dict(type="bar"))
    fig.update_xaxes(
        tickmode='array',
        tickvals=df[dfnames.volume],
        ticktext=[f"{x} ml" for x in df[dfnames.volume].to_list()]
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
