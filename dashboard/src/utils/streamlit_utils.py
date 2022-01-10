from datetime import date, datetime
from typing import List

import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from dateutil.relativedelta import relativedelta
from utils.funcutils import date_range, end_date, start_date

import data.funcdata as dt


def by_day(type_: str, selection: str, countries: List[str]):
    str_countries = ";".join(countries)
    if selection == "Date range":
        date_range_func(type_, str_countries)
    elif selection == "Only a date":
        t_date = st.sidebar.date_input(
            "Pick a date: ", date_range[0], min_value=start_date, max_value=end_date
        )
        df_date = pd.DataFrame(dt.by_date(type_, t_date, str_countries)["countries"])
        df_date = df_date.set_index("country")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.empty()

        with col2:
            st.dataframe(df_date)

        with col3:
            st.empty()

    elif selection == "Date interval":
        date_interval(type_, str_countries)
    else:
        df = pd.DataFrame(
            [dt.last_data(type_, country) for country in countries], index=countries
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.empty()

        with col2:
            st.dataframe(df)

        with col3:
            st.empty()


def by_month(type_: str, selection: str, countries: List[str]):
    str_countries = ";".join(countries)
    if selection == "Month interval":
        year = st.sidebar.number_input(
            label="Select a start year (2020 or 2021)",
            value=2021,
            min_value=2020,
            max_value=2021,
        )
        month = st.sidebar.slider(
            "Select a start month", value=5, min_value=1, max_value=12
        )
        if year == 2021:
            how_months = st.sidebar.slider(
                "Select how many months ", value=1, min_value=0, max_value=13 - month
            )
        else:
            how_months = st.sidebar.slider(
                "Select how many months ", value=1, min_value=1, max_value=12
            )
        start = datetime(year=year, month=month, day=1)
        end = start + relativedelta(months=how_months)

        df_interval = pd.DataFrame(
            dt.m_range(
                type_, start.strftime("%Y-%m"), str_countries, end.strftime("%Y-%m")
            )
        )

        line_chart(df_interval, type_)
        st.write(":heavy_minus_sign:" * 80)
        bar_chart(df_interval, type_)
        st.write(":heavy_minus_sign:" * 80)
        heatmap(df_interval, type_)

    elif selection == "Month range":
        start_year = st.sidebar.number_input(
            label="Select a start year (2020 or 2021)",
            value=2021,
            min_value=2020,
            max_value=2021,
        )
        if start_year:
            start_month = st.sidebar.slider(
                "Select a start month", value=5, min_value=1, max_value=12
            )
        end_year = st.sidebar.number_input(
            label="Select a end year (2020 or 2021)",
            value=start_year,
            min_value=start_year,
            max_value=2021,
        )
        if end_year == start_year:
            end_month = st.sidebar.slider(
                "Select a end month",
                value=start_month + 1,
                min_value=start_month + 1,
                max_value=12,
            )
        else:
            end_month = st.sidebar.slider(
                "Select a end month", value=5, min_value=1, max_value=12
            )
        start = date(year=start_year, month=start_month, day=1)
        end = date(year=end_year, month=end_month, day=1)

        df_range = pd.DataFrame(
            dt.m_range(
                type_, start.strftime("%Y-%m"), str_countries, end.strftime("%Y-%m")
            )
        )
        line_chart(df_range, type_)
        st.write(":heavy_minus_sign:" * 80)
        bar_chart(df_range, type_)
        st.write(":heavy_minus_sign:" * 80)
        heatmap(df_range, type_)


def date_interval(type_: str, str_countries: str):
    t_date = st.sidebar.date_input(
        "Pick a date: ", date_range[0], min_value=start_date, max_value=end_date
    )
    days = st.sidebar.slider(
        "Select how many days ", value=30, min_value=10, max_value=60
    )

    _start_date = t_date

    df = pd.DataFrame(dt.range(type_, _start_date, str_countries, interval=days))

    line_chart(df, type_)
    st.write(":heavy_minus_sign:" * 80)
    bar_chart(df, type_)
    st.write(":heavy_minus_sign:" * 80)
    heatmap(df, type_)


def date_range_func(type_: str, str_countries: str):
    t_date = st.sidebar.date_input(
        "Pick a range date: ", date_range, min_value=start_date, max_value=end_date
    )
    start_date_1 = t_date[0]
    end_date_1 = t_date[-1]
    if t_date[0] > t_date[-1]:
        start_date_1 = t_date[-1]
        end_date_1 = t_date[0]

    df_range = pd.DataFrame(
        dt.range(type_, start_date_1, str_countries, end=end_date_1)
    )

    line_chart(df_range, type_)
    st.write(":heavy_minus_sign:" * 80)
    bar_chart(df_range, type_)
    st.write(":heavy_minus_sign:" * 80)
    heatmap(df_range, type_)


def by_day_all(countries: List[str]):
    str_countries = ";".join(countries)
    t_date = st.sidebar.date_input(
        "Pick a range date: ", date_range, min_value=start_date, max_value=end_date
    )
    start_date_1 = t_date[0]
    end_date_1 = t_date[-1]
    if t_date[0] > t_date[-1]:
        start_date_1 = t_date[-1]
        end_date_1 = t_date[0]

    return pd.DataFrame(dt.range("all", start_date_1, str_countries, end=end_date_1))


def heatmap(df: pd.DataFrame, type_: str):
    pivot = df.pivot(index="country", columns="date", values=type_)
    fig_2, ax = plt.subplots()
    sns.heatmap(pivot, ax=ax)
    st.write("Heatmap chart by country and date:")
    st.pyplot(fig_2)
    with st.expander("See explanation"):
        st.write(
            """
            The chart above shows the heatmap for the cases, deaths or recoveries by
            date and country per day or month.
        """
        )


def line_chart(df: pd.DataFrame, type_: str):
    base = (
        alt.Chart(df)
        .properties()
        .mark_line()
        .encode(x="date", y=type_, color="country")
    )
    st.write("Line chart by country:")
    st.altair_chart(base, use_container_width=True)
    with st.expander("See explanation"):
        st.write(
            """
            The chart above shows a line chart for the cases, deaths or recoveries by
            date and country per day or month.
        """
        )


def bar_chart(df: pd.DataFrame, type_: str):
    fig = px.bar(df, x="country", y=type_)
    st.write("Bar chart by country:")
    st.plotly_chart(fig)
    with st.expander("See explanation"):
        st.write(
            """
            The chart above shows a bar chart for the cases, deaths or recoveries
            aggregated by date and country per day or month.
        """
        )
