import streamlit as st
from utils.streamlit_utils import paint


def app():
    st.title("Deaths")
    st.header("Welcome to the COVID 19 Deaths Page")
    paint("deaths")
