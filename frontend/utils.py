import streamlit as st


def generate_sidebar() -> list:
    """Generates the sidebar with the option. Returns needed variables
    Returns:
        Tuple[bool, bool, Any]:
    """
    st.sidebar.header("Filter CocktailBerry Data")
    st.sidebar.write("Here you can limit the data and filter a little bit")
    st.sidebar.subheader("Countrycodes")
    countrycodes = st.sidebar.radio("Choose Countrycodes", ("A", "B"))
    return countrycodes
