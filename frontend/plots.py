import warnings
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .models import CocktailSchema, InstallationSchema

# ignore the frame.append deprecation warning cause by plotly
warnings.filterwarnings("ignore")
_TREEMAP_HEIGHT = 400
_BARPLOT_HEIGHT = 380


def generate_volume_treemap(df: pd.DataFrame, country_split: bool = True):
    """Uses the language an machine name agg df to generate a treemap"""
    path = [px.Constant("Machines"), CocktailSchema.machine_name]
    if country_split:
        path = [px.Constant("Language used"), CocktailSchema.language, CocktailSchema.machine_name]
    fig = px.treemap(
        df, path=path, values=CocktailSchema.cocktail_volume,
        height=_TREEMAP_HEIGHT, hover_data=[CocktailSchema.cocktail_count]
    )
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata} Cocktails<br>%{value:,.2f} l",
        hovertemplate='%{label}<br>Cocktails Made: %{customdata}<i>x</i><br>Cocktail Volume: %{value:,.2f} l'
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def generate_recipes_treemap(df: pd.DataFrame, country_split: bool = True):
    """Uses the recipe agg df to generate a treemap"""
    path = [px.Constant("Recipes"), CocktailSchema.cocktail_name]
    texttemplate = "<b>%{label}</b> <i>x</i>%{value:.0f}<br>"
    hovertemplate = '%{label}<br>Recipe made: %{value:,.0f}<i>x</i>'
    if country_split:
        path = [px.Constant("Recipes"), CocktailSchema.cocktail_name, CocktailSchema.language]
        texttemplate = "<b>%{parent}</b> <i>x</i>%{value:.0f}<br>(%{label})"
        hovertemplate = '%{parent} (%{label})<br>Recipe made: %{value:,.0f}<i>x</i>'
    fig = px.treemap(df, path=path, values=CocktailSchema.cocktail_count, height=_TREEMAP_HEIGHT)
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    fig.update_traces(
        texttemplate=texttemplate,
        hovertemplate=hovertemplate
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def generate_time_plot(df: pd.DataFrame, machine_grouping: bool):
    """Generates the cocktail count over the time"""
    additional_params = {}
    if machine_grouping:
        additional_params["color"] = CocktailSchema.machine_name
    fig = px.bar(
        df,
        x=CocktailSchema.receivedate,
        y=CocktailSchema.cocktail_count,
        height=_BARPLOT_HEIGHT,
        ** additional_params,
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
    hovertemplate = '<b>%{fullData.name}</b><br>%{label}<br>Cocktails: %{value:i}<i>x</i><extra></extra>'
    fig.update_traces(
        marker_line_width=0,
        selector=dict(type="bar"),
        hovertemplate=hovertemplate
    )
    excluded_days = _generate_excluded_days(df[CocktailSchema.receivedate])
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
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.01
        ),
        rangebreaks=[
            dict(values=excluded_days)  # hide days without values
        ],
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _generate_excluded_days(date_data: pd.Series) -> list[str]:
    """Generates a list of days to exclude from the time plot.
    Leaving only existing dates in the dataframe"""
    start_date = min(date_data)
    end_date = max(date_data)
    delta = end_date - start_date
    used_days = date_data.unique()
    used_days = [pd.to_datetime(day).strftime('%Y-%m-%d') for day in used_days]
    all_days = [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    all_days = [day.strftime('%Y-%m-%d') for day in all_days]
    excluded_days = list(set(all_days) - set(used_days))
    return excluded_days


def generate_serving_size_bars(df: pd.DataFrame, machine_split: bool):
    """Creates a bar chart with the serving sizes"""
    additional_args = {}
    if machine_split:
        additional_args["color"] = CocktailSchema.machine_name
    fig = px.bar(
        df,
        x=CocktailSchema.volume,
        y=CocktailSchema.cocktail_count,
        text_auto=True,
        height=_BARPLOT_HEIGHT,
        **additional_args
    )
    fig.update_layout(
        {"margin": {"l": 0, "r": 0, "t": 0, "b": 0}},
        bargroupgap=0,
        xaxis_title=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )
    hovertemplate = '<b>%{fullData.name}</b><br>Size: %{label}<br>Cocktails: %{value:i}<i>x</i><extra></extra>'
    fig.update_traces(
        marker_line_width=0,
        selector=dict(type="bar"),
        hovertemplate=hovertemplate
    )
    fig.update_xaxes(
        tickmode='array',
        tickvals=df[CocktailSchema.volume],
        ticktext=[f"{x} ml" for x in df[CocktailSchema.volume].to_list()],
        type="category",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def generate_installation_time_chart(df: pd.DataFrame, os_split: bool = False):
    """Shows the cumulative sum of the data over time in a filled line chart"""
    add_args = {}
    if os_split:
        add_args["color"] = InstallationSchema.OS
    fig = px.area(
        df,
        x=InstallationSchema.RECEIVEDATE,
        y=InstallationSchema.INSTALLATIONS_COUNT,
        height=_BARPLOT_HEIGHT,
        **add_args
        # line_shape='spline',
    )
    fig.update_layout(
        {"margin": {"l": 0, "r": 0, "t": 0, "b": 0}},
        hovermode="x unified",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=0
        ),
        xaxis_title=None,
    )
    fig.for_each_trace(lambda trace: trace.update(fillcolor = trace.line.color))
    fig.update_traces(
        hovertemplate='Total Installations: %{y:.0f}',        
    )
    if os_split:
        # Calculate the cumulative sum of INSTALLATIONS_COUNT over time
        os_sum = df.groupby(InstallationSchema.RECEIVEDATE)[InstallationSchema.INSTALLATIONS_COUNT].sum()
        # Add a new trace with the cumulative sum of INSTALLATIONS_COUNT
        fig.add_trace(
            go.Scatter(
                x=os_sum.index,
                y=os_sum,
                mode="lines",
                hovertemplate="%{y:.0f}",
                showlegend=False,
                name="Sum of Installations",
                line={"color": "rgba(0, 0, 0, 0)"},
            )
        )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def generate_installation_treemap(df: pd.DataFrame):
    """Uses the language an machine name agg df to generate a treemap"""
    path = [px.Constant("OS"), InstallationSchema.OS]
    fig = px.treemap(
        df, path=path, values=InstallationSchema.INSTALLATIONS_COUNT,
        height=_TREEMAP_HEIGHT
    )
    fig.update_layout({"margin": {"l": 0, "r": 0, "t": 0, "b": 0}})
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:,.0f} Installation(s)",
        hovertemplate='%{label}<br>Installations: %{value:,.0f}<i>x</i>'
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})