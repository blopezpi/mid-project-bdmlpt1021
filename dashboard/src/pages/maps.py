import time

import pandas as pd
import pydeck as pdk
import streamlit as st
from utils.funcutils import date_range, end_date, start_date

from data.funcdata import get_map


def app():
    selection = st.sidebar.selectbox(
        "Choose one of them:", options=["cases", "deaths", "recoveries"]
    )
    t_date = st.sidebar.date_input(
        "Pick a date: ", date_range[0], min_value=start_date, max_value=end_date
    )
    if st.sidebar.button("Search"):
        spinner()
        df = pd.DataFrame(get_map(selection, t_date))
        layer = pdk.Layer(
            "HeatmapLayer",
            data=df,
            get_position=["longitude", "latitude"],
            get_weight=selection,
            pickable=True,
        )
        view_state = pdk.ViewState(
            longitude=-1.415, latitude=52.2323, zoom=0, max_zoom=10
        )

        r = pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": f"Concentration of {selection} worldwide."},
        )
        st.pydeck_chart(r)


def spinner():
    my_bar = st.progress(0)
    for percent_complete in range(0, 100, 20):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 20)
    my_bar.empty()
