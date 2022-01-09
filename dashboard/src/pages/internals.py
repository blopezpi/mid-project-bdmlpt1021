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
        params["date"] = datetime.combine(st.date_input("Date: "), min.time())

    if objectid and st.button("Update"):
        headers = {"access_token": api_key}
        try:
            result = requests.patch(
                f"{api_uri}/internals/covid/update/{objectid}",
                params=params,
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
    params = {}
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
    params["date"] = datetime.combine(st.date_input("Date: "), min.time())

    if st.button("Insert"):
        headers = {"access_token": api_key}
        try:
            result = requests.put(
                f"{api_uri}/internals/covid/create", params=params, headers=headers
            )
            if result.status_code >= 400:
                st.error(result.text)
            else:
                st.success(result.text)
        except Exception as e:
            st.error(f"Something was wrong: {e}")
