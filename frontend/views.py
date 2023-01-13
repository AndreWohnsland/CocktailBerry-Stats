from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from PIL import Image
import streamlit as st
import pandas as pd

from . import plots
from . import data
from .data import is_dev, DataSchema


LANGUAGE_SPLIT_DESC = "Split by Language Used"
_BASE_PATH = Path(__file__).parent.absolute()
_PICTURE_FOLDER = _BASE_PATH / "assets"


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
    st.sidebar.subheader("🔍 Filter CocktailBerry Data")
    st.sidebar.write("Here you can limit the data and filter a little bit.")
    if df.empty:
        st.sidebar.write("Nothing to do, need some data ...")
        return [], [], [], 1, False, DataFrameStats(0, 0, 0, 0, 0, "No Data", "No Data")
    st.sidebar.subheader("Filter Options")
    st.sidebar.caption("For your Party")
    only_one_day = st.sidebar.checkbox("Only Show last 24h Data", _get_partymode())
    st.sidebar.caption("Basic Settings")
    country_selection = sorted(list(df[DataSchema.language].unique()))
    countrycodes = st.sidebar.multiselect("Choose Used Languages:", country_selection, country_selection)
    machine_selection = sorted(list(df[DataSchema.machine_name].unique()))
    machines = st.sidebar.multiselect("Choose Machines:", machine_selection, machine_selection)
    recipes_selection = sorted(list(df[DataSchema.cocktail_name].unique()))
    recipes_limit = st.sidebar.slider(
        "Show x most Popular Recipes:", 2, max(2, len(recipes_selection)), min(10, len(recipes_selection))
    )
    st.sidebar.caption("Advanced Settings")
    recipes = st.sidebar.multiselect("Choose Recipes:", recipes_selection, recipes_selection)
    # also generates the needed data out of the df
    # since we got unique calculation already here (to save some compute things)
    df_stats = DataFrameStats(
        len(country_selection),
        len(machine_selection),
        len(recipes_selection),
        len(df),
        df[DataSchema.volume].sum() / 1000,
        __build_date(df[DataSchema.receivedate].min()),
        __build_date(df[DataSchema.receivedate].max()),
    )
    return countrycodes, machines, recipes, recipes_limit, only_one_day, df_stats


def _get_partymode() -> bool:
    """Returns if the query requested only data of today"""
    q_params = st.experimental_get_query_params()
    partymode = q_params.get("partymode")
    use_party = partymode is not None and partymode[0].lower() == "true"
    return use_party


def __build_date(checkdate: datetime) -> str:
    yyyymmddfmt = "%a, %d. %b %Y"
    if checkdate.date() == datetime.today().date():
        return "today"
    return checkdate.strftime(yyyymmddfmt)


def display_introduction(df_stats: DataFrameStats):
    """Displays some basic information and stats about the data & project"""
    st.header("🍹CocktailBerry Dashboard")
    st.markdown("Dashboard for all the [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) machines data!")
    with st.expander("What is this?"):
        __what_is_this()
    st.markdown(
        f"""
        ## 📈 Current CocktailBerry Stats
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

        In short, CocktailBerry is a Python software for the Raspberry Pi
        to easily server cocktails and do lots of additional things for your party. The users can send their cocktail data
        (volume, cocktail name) with the according machine data (machine name, language settings) to an API endpoint. ⚙️

        This dashboard will then use the data and visualize it to give you some insights into the data.
        Have a look around on this page, visit the GitHub project, and if you are fond of the project, try it out or even leave a star. ⭐
        """
    )


def display_data(filterd_df: pd.DataFrame, recipes_limit: int, last_day: bool):
    """Generates all the data views (plots and tables) from the data"""
    if filterd_df.empty:
        __say_no_data()
        return
    __show_recipe_data(filterd_df, recipes_limit)
    __show_time_stats(filterd_df, last_day)
    __show_volume_stats(filterd_df)
    __show_serving_size(filterd_df)


def __show_recipe_data(filterd_df: pd.DataFrame, recipes_limit: int):
    """Display Recipes count by recipe and country"""
    st.header("🧾 Recipes Made")
    country_split = st.checkbox(LANGUAGE_SPLIT_DESC, False, key="country_recipe")
    recipe_df = data.cocktail_count(filterd_df, recipes_limit, country_split)
    plots.generate_recipes_treemap(recipe_df, country_split)
    header_addition = " and Language used" if country_split else ""
    with st.expander(f"[Table] Aggregated by {DataSchema.cocktail_name}{header_addition}:"):
        st.table(recipe_df)


def __show_time_stats(filterd_df: pd.DataFrame, last_day: bool):
    """Displays Cocktail count over time"""
    st.header("⏱️ Data Over Time")
    hour_grouping, machine_grouping = __define_granularity(last_day)
    time_df = data.time_aggregation(filterd_df, hour_grouping, machine_grouping)
    plots.generate_time_plot(time_df, machine_grouping)


def __show_volume_stats(filterd_df: pd.DataFrame):
    """Lets the user decide to also split by country code"""
    st.header("🍸 Volume and Number of Cocktails")
    country_split = st.checkbox(LANGUAGE_SPLIT_DESC, False, key="country_machine")
    volume_df = data.sum_volume(filterd_df, country_split)
    plots.generate_volume_treemap(volume_df, country_split)
    header_addition = " Language used and" if country_split else ""
    with st.expander(f"[Table] Aggregated by{header_addition} {DataSchema.machine_name}:"):
        st.table(volume_df.style.format({DataSchema.cocktail_volume: "{:.2f}"}))


def __show_serving_size(filterd_df: pd.DataFrame):
    """Show stats over the prepared volume choices"""
    st.header("🥃 Serving Sizes")
    col1, col2 = st.columns(2)
    machine_split = col1.checkbox("Split by Machine", False, key="serving_machine")
    # only make it available if no machine split is activated
    max_value_posssible = 10
    min_servings: int = col2.slider(
        "Filter Minimal Serving Count", 0,
        max_value_posssible
    )  # type: ignore
    serving_df = data.serving_aggreation(filterd_df, machine_split, min_servings)
    plots.generate_serving_size_bars(serving_df, machine_split)


def __define_granularity(last_day):
    """Lets the user choose in case of all data to aggregate by hour or day"""
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Different Machines?")
        machine_grouping = st.checkbox("Split by Machine", False)
    if last_day:
        return True, machine_grouping
    grouping_options = ("One Day", "One Hour")
    with col2:
        selected_grouping = st.radio(
            "Select the Time Grouping",
            grouping_options
        )
    hour_grouping = selected_grouping == grouping_options[1]
    return hour_grouping, machine_grouping


def __say_no_data():
    """Displays a warning that there is no data to plot"""
    st.warning(
        """
        ⚠️ There is currently no detailed data to be displayed.
        This is probably a result of following reason:

        ❌ Your filtering is too strict and nothing matches the criteria.
        Change your filter or reload the page to reset the filtering.
        """
    )


def display_dev(df):
    """show dev thingies if devmode is on"""
    if is_dev:
        st.header("⚙️ Debug Stuff")
        q_params = st.experimental_get_query_params()
        st.write(q_params)
        with st.expander("All raw Data:"):
            st.table(df)


def display_footer():
    """Generates the footer element with from HTML data"""
    footer = """
    <div class="footer">
        <p class="left">Made with ❤️</p>
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
        __detailed_explanation()


def __detailed_explanation():
    st.markdown(
        """
        #### How To

        The current procedure require you to build your own **CocktailBerry** machine and deliver some kind of proof of its existence.
        The easiest way to do this is to submit a video or some photos of your machine.
        The machine does **NOT** need to be fancy in any way, it should simply work, be able to make cocktails
        and run the CocktailBerry software.
        It does not matter if the pumps are showing or the cabling looks like a mess. 😉

        Please upload your video / photos to some sort of hosting site (Imgur, etc.) and provide the link,
        or give a reference to your blog post (own blog, Reddit, social media) if you did such things for your machine.
        It would be nice to write some words in addition to the submission, even if it's just a kind greeting,
        and provide me some sort of name or alias how should I reply to you (first name or your preferred alias is fine).
        You can [contact me](mailto:cocktailmakeraw@gmail.com) for further questions or just to get the API-key.

        #### Why a Protected API

        The reason behind this is that only **real machines** should submit data for the dashboard (you could otherwise
        just run the Python program anywhere and submit a lot of data) and to minimize any other kinds of exploits
        of the API. There is no option to submit a photo (the implementation here would be quite simple) because this could
        also be exploited quite easily. The internet is still a wild and scary place! 🦖
        Also, I would love to see what you did in combination with my software.

        #### Final Steps

        You can then use the received API key for the CocktailBerry microservice (in the .env file).
        As soon as there is a valid key and the microservice is enabled, your machine will send the cocktail data
        (*cocktail name, machine name, volume and language setting*) to the API using the API-key.
        The activation of this feature is also explained in the CocktailBerry docs.

        #### Will this be Easier in the Future

        I always work on improvements and try to bring the most joy with CocktailBerry and related projects.
        Since I do it all in my free time + open source, sadly my time is limited, and I can only do so much.
        If you may know a better way, feel free to contact me and let's start a nice discussion to make the
        CocktailBerry environment even better!
        """
    )


def display_machine_types():
    """Shows the different machine types which were submitted"""
    st.header("🤖 Existing Machines")
    st.markdown("Here are some of the machines which were build and are used. Maybe they inspired you to build your own?")
    with st.expander("CocktailBerry Mk 1"):
        _display_cocktailberry_mk_one()
    with st.expander("CocktailBerry Mk 2"):
        _display_cocktailberry_mk_two()


def _display_cocktailberry_mk_one():
    """Shows information about the first CocktailBerry machine"""
    description = """**CocktailBerry Mk 1** was the start of the journey and the birth of this project.
        It got 10 12V Pumps, a Raspberry Pi 3b+, relays to control the pumps and a 5-inch touch screen.
        The casing is made out of stainless steel, the electric is inside an electric box for protection as well as display.
        The pumps are located above the bottles.
    """
    _generate_machine_info("Andre Wohnsland", description)
    _display_picture("cbmk1.jpg", "Good old CocktailBerry Mk 1")


def _display_cocktailberry_mk_two():
    """Shows information about the second CocktailBerry machine"""
    description = """**CocktailBerry Mk 2** is the successor of the first model.
        The pumps were reduced to 8, to make it smaller and better portable.
        The design was changed to be more modern and for production on a 3D printer.
        The screen is now a 7-inch touch screen, for better user experience.
        There is also only one power supply, a 12V one for the supply of the pumps.
        The current gets split and converted into a 5V one, which is enough for the RPi to run.
        The pumps are still located above the bottles.
        The machine is mounted on a wooden plate for stability and can be disassembled easily for transport.
    """
    _generate_machine_info("Andre Wohnsland", description)
    _display_picture("cbmk2.jfif", "Fancy newer CocktailBerry Mk 2")


def _generate_machine_info(maker, description):
    st.markdown(
        f"""
        <ins>_Maker_</ins>:<br>
        **{maker}**

        <ins>_Description_</ins>:<br>
        {description}

        <ins>_Pictures_</ins>:
        """, unsafe_allow_html=True)


def _display_picture(picture_name: str, caption: str):
    """Displays the given picture with the given caption
    Uses the assets folder as base path"""
    picture_path = _PICTURE_FOLDER / picture_name
    image = Image.open(picture_path)
    st.image(image, caption=caption, use_column_width=True)
