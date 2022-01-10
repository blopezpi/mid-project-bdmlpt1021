import json
from datetime import datetime

import requests
import streamlit as st
from config import api_key, api_uri, user_pass


def app():
    password = st.text_input("Enter a password", type="password")
    if password == user_pass:
        select = st.sidebar.selectbox(
            "Select one of the following options:",
            options=["Delete a row", "Update a row", "Insert a row"],
        )
        if select == "Delete a row":
            delete()
        elif select == "Update a row":
            update()
        else:
            insert()


def delete():
    objectid = st.text_input("Introduce the objectid to delete: ")
    if objectid and st.button("Delete"):
        headers = {"access_token": api_key}
        try:
            result = requests.delete(
                f"{api_uri}/internals/covid/delete/{objectid}", headers=headers
            )
            if result.status_code >= 400:
                st.error(result.text)
            else:
                st.success(result.text)
        except Exception as e:
            st.error(f"Something was wrong: {e}")


def update():
    objectid = st.text_input("Introduce the objectid to update: ")
    params = {}
    if objectid:
        country = st.text_input("New country:")
        if country:
            params["country"] = country

        latitude = st.number_input("New latitude:", format="%.2f")
        if latitude:
            params["latitude"] = latitude
        longitude = st.number_input("New longitude:", format="%.2f")
        if longitude:
            params["longitude"] = longitude

        cases = st.number_input("Cases: ", step=1, format="%i")
        if cases:
            params["cases"] = cases

        deaths = st.number_input("Deaths: ", step=1, format="%i")
        if deaths:
            params["deaths"] = deaths

        recoveries = st.number_input("Recoveries: ", step=1, format="%i")
        if recoveries:
            params["recoveries"] = recoveries

        cases_accumulated = st.number_input("Cases accumulated: ", step=1, format="%i")
        if cases_accumulated:
            params["cases_accumulated"] = cases_accumulated

        deaths_accumulated = st.number_input(
            "Deaths acccumulated: ", step=1, format="%i"
        )
        if deaths_accumulated:
            params["deaths_accumulated"] = deaths_accumulated

        recoveries_accumulated = st.number_input(
            "Recoveries accumulated: ", step=1, format="%i"
        )
        if recoveries_accumulated:
            params["recoveries_accumulated"] = recoveries_accumulated
        date_select = st.selectbox("Update the date:", options=["Yes", "No"])
        if date_select == "Yes":
            params["date"] = datetime.combine(
                st.date_input("Date: "), datetime.min.time()
            ).isoformat()

        if longitude and latitude:
            params["location"] = {}
            params["location"]["type"] = "Point"
            params["location"]["coordinates"] = [
                params["longitude"],
                params["latitude"],
            ]

    if objectid and st.button("Update"):
        headers = {
            "access_token": api_key,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            result = requests.patch(
                f"{api_uri}/internals/covid/update/{objectid}",
                data=json.dumps(params),
                headers=headers,
            )
            if result.status_code >= 400:
                st.error(result.text)
            else:
                st.success(result.text)
        except Exception as e:
            st.error(f"Something was wrong: {e}")


def insert():
    st.write("Inserting a new row in the database")
    params = {"location": {"type": "Point"}}
    params["country"] = st.text_input("New country:")
    params["latitude"] = st.number_input("New latitude:", format="%.2f")
    params["longitude"] = st.number_input("New longitude:", format="%.2f")
    params["cases"] = st.number_input("Cases: ", step=1, format="%i")
    params["deaths"] = st.number_input("Deaths: ", step=1, format="%i")
    params["recoveries"] = st.number_input("Recoveries: ", step=1, format="%i")
    params["cases_accumulated"] = st.number_input(
        "Cases accumulated: ", step=1, format="%i"
    )
    params["deaths_accumulated"] = st.number_input(
        "Deaths acccumulated: ", step=1, format="%i"
    )
    params["recoveries_accumulated"] = st.number_input(
        "Recoveries accumulated: ", step=1, format="%i"
    )
    params["date"] = datetime.combine(
        st.date_input("Date: "), datetime.min.time()
    ).isoformat()
    params["location"]["coordinates"] = [params["longitude"], params["latitude"]]
    if st.button("Insert"):
        headers = {
            "access_token": api_key,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            result = requests.put(
                f"{api_uri}/internals/covid/create",
                data=json.dumps(params),
                headers=headers,
            )
            if result.status_code >= 400:
                st.error(result.text)
            else:
                st.success(result.text)
        except Exception as e:
            st.error(f"Something was wrong: {e}")
