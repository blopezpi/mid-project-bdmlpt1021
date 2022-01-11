import streamlit as st
from utils.streamlit_utils import paint


def app():
    st.title("Recoveries")
    st.header("Welcome to the COVID 19 Recoveries Page")
    st.markdown(
        """
        This page is going to be discontinued because the recovery data is not receiving updates anymore.
        The only country that is currently receiving updates is Canada.
        The rest of the countries recovery data have not receive updates since 2021,
        but there is data available from previous years.
    """
    )
    paint("recoveries")
