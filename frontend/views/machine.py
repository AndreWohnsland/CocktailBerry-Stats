from dataclasses import dataclass
from pathlib import Path

import streamlit as st

_PICTURE_FOLDER = Path(__file__).parents[1].absolute() / "assets"
_NAME_AW = "Andre Wohnsland"


@dataclass
class _Machine:
    name: str
    maker: str
    description: str
    pictures: list[tuple[str, str]]
    """List of (file name in the assets folder, caption)."""


_MACHINES = [
    _Machine(
        name="CocktailBerry Mk 1",
        maker=_NAME_AW,
        description="""**CocktailBerry Mk 1** was the start of the journey and the birth of this project.
        It got 10 12V Pumps, a Raspberry Pi 3b+, relays to control the pumps and a 5-inch touch screen.
        The casing is made out of stainless steel,
        the electric is inside an electric box for protection as well as display.
        The pumps are located above the bottles.
        """,
        pictures=[("cbmk1.jpg", "Good old CocktailBerry Mk 1")],
    ),
    _Machine(
        name="CocktailBerry Mk 2",
        maker=_NAME_AW,
        description="""**CocktailBerry Mk 2** is the successor of the first model.
        The pumps were reduced to 8, to make it smaller and better portable.
        The design was changed to be more modern and for production on a 3D printer.
        The screen is now a 7-inch touch screen, for better user experience.
        There is also only one power supply, a 12V one for the supply of the pumps.
        The current gets split and converted into a 5V one, which is enough for the RPi to run.
        The pumps are still located above the bottles.
        The machine is mounted on a wooden plate for stability and can be disassembled easily for transport.
        """,
        pictures=[("cbmk2.jpg", "Fancy newer CocktailBerry Mk 2"), ("cbmk2-2.jpg", "Machine in action")],
    ),
    _Machine(
        name="CocktailBerry Mk 3",
        maker=_NAME_AW,
        description="""**CocktailBerry Mk 3** is the next step from Mk2.
        The build is quite identical to the previous model, so there is no big change in shape or concept.
        However, the parts got a good chunk smaller.
        This is thanks to the custom CocktailBerry board, which replaces the old relay array.
        With this, less inside build volume is needed, which reduces top diameter from 320 to 240 mm.
        This also reduced needed PLA from ~3 to ~2 kg, and makes production on smaller 3D printers possible.
        The model also got some WS281x ring LEDs build in, for some RGB action and inserted threads for more durability.
        """,
        pictures=[("cbmk3.jpg", "Next Iteration: CocktailBerry Mk 3"), ("cbmk3-2.jpg", "Additional Side View")],
    ),
    _Machine(
        name="CocktailBerry 2Go",
        maker=_NAME_AW,
        description="""**CocktailBerry 2Go** is a portable version of the CocktailBerry machine series.
        The machine is designed to be easily transportable and to be used on the go.
        It is built into a euro box, which can be closed and carried around.
        A custom PCB (CocktailBerryBoard Slim) was designed to control the pumps.
        In this case, a RockPi was used instead of a Raspberry Pi, since it has 12V input and does not need a converter.
        From a personal view, I would not recommend this board to a beginner,
        as it is harder to setup and may have some issues on the software side.
        """,
        pictures=[("cb2go.jpg", "CocktailBerry 2Go: Front view")],
    ),
    _Machine(
        name="Bart",
        maker="Thomas",
        description="""The basic structure of the cocktail machine consists of wooden slats and screen printing plates,
        on which a black plastic covering has been attached.
        Inside there are 8 water pumps (12V) which transport the ingredients through food save hoses.
        On top sits a box made of transparent acrylic glass, which contains the electric hardware.
        This includes: Raspberry Pi 3 Model B, 7 inch HDMI IPS touchscreen (1024x600),
        8 channel relay module, power distribution board and step-down module, as well as a LED strip.
        The other parts were all created using 3D printing.
        The bottles are located on both sides of the machine.
        """,
        pictures=[("bart.jpg", "Bart: Front view"), ("bart-2.jpg", "It's short for Bartender")],
    ),
    _Machine(
        name="Alumat",
        maker="Thomas",
        description="""The structure is built from 15 meters of black aluminum profiles (B-type, 20x20mm),
        connected with various brackets.
        At the core is a Raspberry Pi 3 B+, powered with its official power supply to avoid known voltage issues.
        The Pi controls two 8-channel 5V relays, powering a total of 16 membrane pumps (12V).
        Due to unavailability of smaller pumps, larger ones are used this time, but there's enough space for them.
        A 7-inch mini touchscreen (1024x600) is used for operation and display.
        The electronics are housed in a 3mm thick plexiglass case.
        Two LED fans were planned for the case, but due to power supply issues, an LED strip was used instead.
        The mounting brackets for the 16 pumps, the tube funnel, labels, and various spacers were 3D-printed from PLA.
        """,
        pictures=[("alumat.jpg", "Alumat: Front view"), ("alumat-2.jpg", "Quite a solid build")],
    ),
    _Machine(
        name="AlcoholFactory",
        maker="ChrisOle",
        description="""The housing of the machine was assembled from powder-coated sheet metal and aluminum rails.
        The technology inside comprises a Raspberry Pi 4 with a 7-inch IPS touch display.
        The 16 pumps are controlled via 12V relays.
        Four of the pumps are peristaltic pumps designed to handle thicker liquids,
        such as juices and grenadine syrup more effectively (thus ensuring longer runtime).
        The remaining 12 pumps are cheaper and faster water pumps.
        The containers for the liquids were self-designed and 3D printed using food-grade PETG material.
        To ensure food safety, the components that come into contact with the liquid were coated with food-grade epoxy.
        """,
        pictures=[
            ("alcohol_factory1.jpg", "Front view, it's nice"),
            ("alcohol_factory3.jpg", "Solved the bottle problem"),
        ],
    ),
]


def display_machine_types() -> None:
    """Show the different machine types which were submitted."""
    st.header("🤖 Existing Machines")
    st.markdown(
        "Here are some of the machines which were build and are used. Maybe they inspired you to build your own?"
    )
    for machine in sorted(_MACHINES, key=lambda m: m.name):
        with st.expander(machine.name):
            _display_machine(machine)


def _display_machine(machine: _Machine) -> None:
    st.markdown(
        f"""
        <ins>_Maker_</ins>:<br>
        **{machine.maker}**

        <ins>_Description_</ins>:<br>
        {machine.description}

        <ins>_Pictures_</ins>:
        """,
        unsafe_allow_html=True,
    )
    containers = st.columns(len(machine.pictures)) if len(machine.pictures) > 1 else [st]
    for container, (file_name, caption) in zip(containers, machine.pictures, strict=True):
        container.image(str(_PICTURE_FOLDER / file_name), caption=caption, width="stretch")
