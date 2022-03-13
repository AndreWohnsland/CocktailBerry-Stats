import warnings
import pandas as pd
import plotly.express as px
import streamlit as st

# ignore the frame.append deprecation warning cause by plotly
warnings.filterwarnings("ignore")


def generate_volume_treemap(df: pd.DataFrame):
    fig = px.treemap(df, path=[px.Constant("Countrycodes"), 'Countrycode', 'Machinename'],
                     values="Cocktail Volume in ml", height=400)
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    st.plotly_chart(fig, use_container_width=True)


def generate_recipes_treemap(df: pd.DataFrame):
    fig = px.treemap(df, path=[px.Constant("Recipes"), "Cocktailname", 'Countrycode'],
                     values="Number of Cocktails", height=400)
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    st.plotly_chart(fig, use_container_width=True)
