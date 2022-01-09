import streamlit as st
from utils.streamlit_utils import by_day, by_month

import data.funcdata as dt


def app():
    st.title("Deaths")
    st.header("Welcome to the COVID 19 Deaths Page")
    st.write(":heavy_minus_sign:" * 50)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.empty()

    with col2:
        last = dt.last_data("deaths")

        total = last["deaths_accumulated"]
        delta = last["deaths"]
        with st.container():
            st.metric(
                label=f'Last deaths registered in the world at {last["date"]}',
                value=total,
                delta=delta,
                delta_color="inverse",
            )

    with col3:
        st.empty()

    st.write(":heavy_minus_sign:" * 50)

    countries = st.sidebar.multiselect(
        "Select one or more countries (max 10): ", options=dt.get_countries()
    )
    if countries:
        countries = countries[:9]
    else:
        st.stop()

    selection = st.sidebar.radio(
        "Select one of the following options to view:", options=["By month", "By day"]
    )

    select = ""

    if selection == "By month":
        select = st.sidebar.selectbox(
            "Select one of the following options:",
            options=["Month interval", "Month range"],
        )
        by_month("deaths", select, countries)
    else:
        select = st.sidebar.selectbox(
            "Select one of the following options:",
            options=["Date interval", "Date range", "Only a date", "Last day"],
        )
        by_day("deaths", select, countries)
