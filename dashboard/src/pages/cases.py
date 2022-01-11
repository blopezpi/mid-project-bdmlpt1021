import streamlit as st
from utils.streamlit_utils import paint


def app():
    st.title("Cases")
    st.header("Welcome to the COVID 19 Cases Page")
    paint("cases")
