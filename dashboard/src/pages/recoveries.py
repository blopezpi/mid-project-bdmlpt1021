import streamlit as st
from utils.streamlit_utils import by_day, by_month

import data.funcdata as dt


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
    st.write(":heavy_minus_sign:" * 80)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.empty()

    with col2:
        last = dt.last_data("recoveries")

        total = last["recoveries_accumulated"]
        delta = last["recoveries"]

        with st.container():
            st.metric(
                label=f'Last recoveries registered in the world at {last["date"]}',
                value=total,
                delta=delta,
            )

    with col3:
        st.empty()

    st.write(":heavy_minus_sign:" * 80)

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
        by_month("recoveries", select, countries)
    else:
        select = st.sidebar.selectbox(
            "Select one of the following options:",
            options=["Date interval", "Date range", "Only a date", "Last day"],
        )
        by_day("recoveries", select, countries)
