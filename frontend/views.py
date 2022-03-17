from dataclasses import dataclass
from datetime import datetime
import streamlit as st
import pandas as pd

from data import sum_volume, cocktail_count, is_dev, dfnames
from plots import generate_volume_treemap, generate_recipes_treemap


@dataclass
class DataFrameStats():
    countries: int
    machines: int
    recipes: int
    cocktails: int
    volume: int
    first_data: str
    last_data: str


def generate_sidebar(df: pd.DataFrame):
    """Generates the sidebar with the option. Returns needed variables"""
    st.sidebar.header("🔍 Filter CocktailBerry Data")
    st.sidebar.write("Here you can limit the data and filter a little bit.")
    if df.empty:
        st.sidebar.write("Nothing to do, need some data ...")
        return [], [], [], 1, DataFrameStats(0, 0, 0, 0, 0, "No Data", "No Data")
    st.sidebar.subheader("Filter Options")
    country_selection = sorted(list(df[dfnames.language].unique()))
    countrycodes = st.sidebar.multiselect("Choose Used Languages:", country_selection, country_selection)
    machine_selection = sorted(list(df[dfnames.machine_name].unique()))
    machines = st.sidebar.multiselect("Choose Machines:", machine_selection, machine_selection)
    recipes_selection = sorted(list(df[dfnames.cocktail_name].unique()))
    recipes_limit = st.sidebar.slider(
        "Show x most popular recipes:", 2, max(2, len(recipes_selection)), min(10, len(recipes_selection))
    )
    recipes = st.sidebar.multiselect("Choose Recipes:", recipes_selection, recipes_selection)
    # also generates the needed data out of the df
    # since we got unique calculation already here (to save some compute things)
    df_stats = DataFrameStats(
        len(country_selection),
        len(machine_selection),
        len(recipes_selection),
        len(df),
        df[dfnames.volume].sum() / 1000,
        __build_date(df[dfnames.receivedate].min()),
        __build_date(df[dfnames.receivedate].max()),
    )
    return countrycodes, machines, recipes, recipes_limit, df_stats


def __build_date(checkdate: datetime) -> str:
    yyyymmddfmt = "%Y-%m-%d"
    if checkdate.date() == datetime.today().date():
        return "today"
    return checkdate.strftime(yyyymmddfmt)


def display_introduction(df_stats: DataFrameStats):
    """Displays some basic information and stats about the data & project"""
    st.title("🍹CocktailBerry Dashboard")
    st.markdown("Dashboard for all the [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) machines data!")
    with st.expander("What is this?"):
        __what_is_this()
    st.markdown(
        f"""
        # 📈 Current CocktailBerry Stats
        - 🍸 **{df_stats.cocktails}** cocktails made
        - 🧾 **{df_stats.recipes}** different recipes tasted
        - 🎊 **{df_stats.volume:.1f}** litre cocktails produced
        - 🕹️ **{df_stats.machines}** machines sending data
        - 🌐 **{df_stats.countries}** languages used
        - 🧊 oldest data: **{df_stats.first_data}**
        - 🔥 latest data: **{df_stats.last_data}**
        """
    )


def __what_is_this():
    """Returns some additional information about the dashboard"""
    st.markdown(
        """
        This is the official WebApp / Dashboard for the [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) project.
        If you don't know it, go check it out, it's super cool. 🚀

        In short, CocktailBerry is a Python software for the Rapsberry Pi
        to easily server cocktails and do lots of additional things for your party. The users can send their cocktail data
        (volume, cocktail name) with the according machine data (machine name, language settings) to an API endpoint. ⚙️

        This dashboard will then use the data and visualize it to give you some insights into the data.
        Have a look around on this page, visit the GitHub project, and if you are fond of the project, try it out or even leave a star. ⭐
        """
    )


def display_data(filterd_df: pd.DataFrame, recipes_limit: int):
    """Generates all the data views (plots and tables) from the data"""
    volume_df = sum_volume(filterd_df)
    recipe_df = cocktail_count(filterd_df, recipes_limit)

    # Display section of volume / count data
    st.header("🍸 Volume and Number of Cocktails")
    if not volume_df.empty:
        generate_volume_treemap(volume_df)
    else:
        __say_no_data()
    with st.expander(f"[Table] Aggregated by Language used and {dfnames.machine_name}:"):
        st.table(volume_df.style.format({dfnames.cocktail_volume: "{:.2f}"}))

    # Display section of recipe data
    st.header("🧾 Recipes Made")
    if not recipe_df.empty:
        generate_recipes_treemap(recipe_df)
    else:
        __say_no_data()
    with st.expander(f"[Table] Aggregated by {dfnames.cocktail_name} and Language used (Top {recipes_limit}):"):
        st.table(recipe_df)


def __say_no_data():
    """Displays a warning that there is no data to plot"""
    st.warning(
        """
        ⚠️ There is currently no data to be displayed. This is probably a result of following reason:

        - ❌ Your filtering is too strict and nothing matches the criteria. Change your filter or reload the page to reset the filtering.
        """
    )


def display_dev(df):
    """show dev thingies if devmode is on"""
    if is_dev:
        st.header("⚙️ Debug Stuff")
        with st.expander("All raw Data:"):
            st.table(df)


def display_footer():
    """Generates the footer element with from HTML data"""
    footer = """
    <div class="footer">
        <p class="left">Developed with ❤️</p>
        <p class="right">Data from <a href="https://github.com/AndreWohnsland/CocktailBerry">CocktailBerry</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)


def display_api_instructions():
    """Shows the needed information to get the API key for CocktailBerry"""
    st.header("❓ How to participate")
    st.markdown(
        """
        The tl;dr is you need to build your own [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry)
        machine and install the software on it. After that, you provide me proof that it exists / works  (video / pictures /
        blog or social media post). Afterwards, you will get an API key to submit your machine data.
        """)
    with st.expander("Show details and reasons behind them:"):
        st.markdown(
            """
            #### How To

            The current procedure require you to build your own **CocktailBerry** machine and deliver some kind of proof of its existence.
            The easiest way to do this is to submit a video or some photos of your machine.
            The machine does **NOT** need to be fancy in any way, it should simply work, be able to make cocktails
            and run the CocktailBerry software.
            It does not matter if the pumps are showing or the cabling looks like a mess. 😉

            Please upload your video / photos to some sort of hosting site (Imgur, etc.) and provide the link,
            or give a reference to your blogpost (own blog, Reddit, social media) if you did such things for your machine.
            It would be nice to write some words in addition to the submission, even if it's just a kind greeting,
            and provide me some sort of name or alias how should I reply to you (first name or your preferred alias is fine).
            You can [contact me](mailto:cocktailmakeraw@gmail.com) for further questions or just to get the API-key.

            #### Why a protected API

            The reason behind this is that only **real machines** should submit data for the dashboard (you could otherwise
            just run the Python program anywhere and submit a lot of data) and to minimize any other kinds of exploits
            of the API. There is no option to submit a photo (the implementation here would be quite simple) because this could
            also be exploited quite easily. The internet is still a wild and scary place! 🦖
            Also, I would love to see what you did in combination with my software.

            #### Final steps

            You can then use the received API key for the CocktailBerry microservice (in the .env file).
            As soon as there is a valid key and the microservice is enabled, your machine will send the cocktail data
            (*cocktail name, machine name, volume and language setting*) to the API using the API-key.
            The activation of this feature is also explained in the CocktailBerry docs.

            #### Will this be easier in the future

            I always work on improvements and try to bring the most joy with CocktailBerry and related projects.
            Since I do it all in my free time + open source, sadly my time is limited, and I can only do so much.
            If you may know a better way, feel free to contact me and let's start a nice discussion to make the
            CocktailBerry environment even better!
            """
        )
