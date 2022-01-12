import streamlit as st
from multiapp import MultiApp
from pages import cases, deaths, home, internals, maps, recoveries, report
from sentry import set_sentry

set_sentry()

st.set_page_config(
    layout="wide",
    menu_items={
        "Get Help": "https://github.com/blopezpi/mid-project-bdmlpt1021/blob/main/README.md",
        "Report a bug": "https://github.com/blopezpi/mid-project-bdmlpt1021/issues",
        "About": "# Welcome to Covid 19 Dashboard!",
    },
)

app = MultiApp()

app.add_pages("Home", home.app)
app.add_pages("Cases", cases.app)
app.add_pages("Recoveries", recoveries.app)
app.add_pages("Deaths", deaths.app)
app.add_pages("Report", report.app)
app.add_pages("Maps", maps.app)
app.add_pages("Internals", internals.app)

app.run()
