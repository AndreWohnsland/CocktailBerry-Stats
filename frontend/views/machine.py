from pathlib import Path
from PIL import Image
import streamlit as st

_BASE_PATH = Path(__file__).parents[1].absolute()
_PICTURE_FOLDER = _BASE_PATH / "assets"


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
