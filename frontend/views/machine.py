from pathlib import Path
from typing import TYPE_CHECKING, Optional

import streamlit as st
from PIL import Image

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator

_BASE_PATH = Path(__file__).parents[1].absolute()
_PICTURE_FOLDER = _BASE_PATH / "assets"
_NAME_AW = "Andre Wohnsland"


def display_machine_types():
    """Show the different machine types which were submitted."""
    st.header("🤖 Existing Machines")
    st.markdown(
        "Here are some of the machines which were build and are used. Maybe they inspired you to build your own?"
    )
    machine_data = [
        ("CocktailBerry Mk 1", _display_cocktailberry_mk_one),
        ("CocktailBerry Mk 2", _display_cocktailberry_mk_two),
        ("CocktailBerry Mk 3", _display_cocktailberry_mk_three),
        ("CocktailBerry 2Go", display_cocktailberry_2go),
        ("Bart", _display_bart),
        ("AlcoholFactory", _display_alcohol_factory),
    ]
    for name, function in machine_data:
        with st.expander(name):
            function()


def _display_cocktailberry_mk_one():
    """Show information about the first CocktailBerry machine."""
    description = """**CocktailBerry Mk 1** was the start of the journey and the birth of this project.
        It got 10 12V Pumps, a Raspberry Pi 3b+, relays to control the pumps and a 5-inch touch screen.
        The casing is made out of stainless steel,
        the electric is inside an electric box for protection as well as display.
        The pumps are located above the bottles.
    """
    _generate_machine_info(_NAME_AW, description)
    _display_picture("cbmk1.jpg", "Good old CocktailBerry Mk 1")


def _display_cocktailberry_mk_two():
    """Show information about the second CocktailBerry machine."""
    description = """**CocktailBerry Mk 2** is the successor of the first model.
        The pumps were reduced to 8, to make it smaller and better portable.
        The design was changed to be more modern and for production on a 3D printer.
        The screen is now a 7-inch touch screen, for better user experience.
        There is also only one power supply, a 12V one for the supply of the pumps.
        The current gets split and converted into a 5V one, which is enough for the RPi to run.
        The pumps are still located above the bottles.
        The machine is mounted on a wooden plate for stability and can be disassembled easily for transport.
    """
    _generate_machine_info(_NAME_AW, description)
    col1, col2 = st.columns(2)
    _display_picture("cbmk2.jpg", "Fancy newer CocktailBerry Mk 2", col1)
    _display_picture("cbmk2-2.jpg", "Machine in action", col2)


def _display_cocktailberry_mk_three():
    """Show information about the second CocktailBerry machine."""
    description = """**CocktailBerry Mk 3** is the next step from Mk2.
        The build is quite identical to the previous model, so there is no big change in shape or concept.
        However, the parts got a good chunk smaller.
        This is thanks to the custom CocktailBerry board, which replaces the old relay array.
        With this, less inside build volume is needed, which reduces top diameter from 320 to 240 mm.
        This also reduced needed PLA from ~3 to ~2 kg, and makes production on smaller 3D printers possible.
        The model also got some WS281x ring LEDs build in, for some RGB action and inserted threads for more durability.
    """
    _generate_machine_info(_NAME_AW, description)
    col1, col2 = st.columns(2)
    _display_picture("cbmk3.jpg", "Next Iteration: CocktailBerry Mk 3", col1)
    _display_picture("cbmk3-2.jpg", "Additional Side View", col2)


def display_cocktailberry_2go():
    """Show information about the CocktailBerry 2Go machine."""
    description = """**CocktailBerry 2Go** is a portable version of the CocktailBerry machine series.
        The machine is designed to be easily transportable and to be used on the go.
        It is built into a euro box, which can be closed and carried around.
        A custom PCB (CocktailBerryBoard Slim) was designed to control the pumps.
        In this case, a RockPi was used instead of a Raspberry Pi, since it has 12V input and does not need a converter.
        From a personal view, I would not recommend this board to a beginner,
        as it is harder to setup and may have some issues on the software side.
    """
    _generate_machine_info(_NAME_AW, description)
    _display_picture("cb2go.jpg", "CocktailBerry 2Go: Front view")


def _display_bart():
    """Show information about bart."""
    description = """ The basic structure of the cocktail machine consists of wooden slats and screen printing plates,
        on which a black plastic covering has been attached.
        Inside there are 8 water pumps (12V) which transport the ingredients through food save hoses.
        On top sits a box made of transparent acrylic glass, which contains the electric hardware.
        This includes: Raspberry Pi 3 Model B, 7 inch HDMI IPS touchscreen (1024x600),
        8 channel relay module, power distribution board and step-down module, as well as a LED strip.
        The other parts were all created using 3D printing.
        The bottles are located on both sides of the machine.
    """
    _generate_machine_info("Thomas", description)
    col1, col2 = st.columns(2)
    _display_picture("bart.jpg", "Bart: Front view", col1)
    _display_picture("bart-2.jpg", "It's short for Bartender", col2)


def _display_alcohol_factory():
    """Show information about AlcoholFactory."""
    description = """ The housing of the machine was assembled from powder-coated sheet metal and aluminum rails.
        The technology inside comprises a Raspberry Pi 4 with a 7-inch IPS touch display.
        The 16 pumps are controlled via 12V relays.
        Four of the pumps are peristaltic pumps designed to handle thicker liquids,
        such as juices and grenadine syrup more effectively (thus ensuring longer runtime).
        The remaining 12 pumps are cheaper and faster water pumps.
        The containers for the liquids were self-designed and 3D printed using food-grade PETG material.
        To ensure food safety, the components that come into contact with the liquid were coated with food-grade epoxy.
    """
    _generate_machine_info("ChrisOle", description)
    col1, col2 = st.columns(2)
    _display_picture("alcohol_factory1.jpg", "Front view, it's nice", col1)
    _display_picture("alcohol_factory3.jpg", "Solved the bottle problem", col2)


def _generate_machine_info(maker, description):
    st.markdown(
        f"""
        <ins>_Maker_</ins>:<br>
        **{maker}**

        <ins>_Description_</ins>:<br>
        {description}

        <ins>_Pictures_</ins>:
        """,
        unsafe_allow_html=True,
    )


def _display_picture(picture_name: str, caption: str, container: Optional["DeltaGenerator"] = None):
    """Display the given picture with the given caption.

    Uses the assets folder as base path.
    """
    picture_path = _PICTURE_FOLDER / picture_name
    image = Image.open(picture_path)
    if container is not None:
        container.image(image, caption=caption, use_column_width=True)
        return
    st.image(image, caption=caption, use_column_width=True)
