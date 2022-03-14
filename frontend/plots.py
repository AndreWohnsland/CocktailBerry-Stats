import warnings
import pandas as pd
import plotly.express as px
import streamlit as st

# ignore the frame.append deprecation warning cause by plotly
warnings.filterwarnings("ignore")


def generate_volume_treemap(df: pd.DataFrame):
    fig = px.treemap(df, path=[px.Constant("Language used"), 'Language', 'Machine Name'],
                     values="Cocktail Volume in Litre", height=400)
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:,.2f} l",
        hovertemplate='%{label}<br>Cocktail Volume: %{value:,.2f} l'
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def generate_recipes_treemap(df: pd.DataFrame):
    fig = px.treemap(df, path=[px.Constant("Recipes"), "Cocktailname", 'Language'],
                     values="Number of Cocktails", height=400)
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    fig.update_traces(
        texttemplate="<b>%{parent}</b> <i>x</i>%{value:.0f}<br>(%{label})",
        hovertemplate='%{parent} (%{label})<br>Repice made: %{value:,.0f}'
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
