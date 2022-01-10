import base64
import os
import re

import jinja2
import pdfkit
import streamlit as st
from config import user_pass
from mailjet_rest import Client
from utils.streamlit_utils import by_day_all

import data.funcdata as dt


def app():
    countries = st.sidebar.multiselect(
        "Select one or more countries (max 10): ", options=dt.get_countries()
    )

    if countries:
        df = by_day_all(countries)
        df.sort_values(by=["date"], inplace=True)
        df.drop(
            columns=[
                "recoveries_accumulated",
                "deaths_accumulated",
                "cases_accumulated",
            ],
            inplace=True,
        )
        templateLoader = jinja2.FileSystemLoader(searchpath="./pages")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "pdf_report.html"
        template = templateEnv.get_template(TEMPLATE_FILE)

        outputText = template.render(df=df)
        html_file = open("pdf_report_table.html", "w")
        html_file.write(outputText)
        html_file.close()

        pdfkit.from_file("pdf_report_table.html", "pdf_report.pdf")
        with open("pdf_report.pdf", "rb") as pdf:
            st.download_button("Download report", data=pdf, file_name="report.pdf")
        password = st.text_input(
            "Enter a password to send you a mail with the report.", type="password"
        )
        if password == user_pass:
            mail = st.text_input(
                "If you prefer you can get the report to your mail (Please provide us): "
            )
            if st.button("Send by mail"):
                if re.fullmatch(r"^[^@]+@[^@]+\.[^@]+$", mail):
                    send_mail(mail, "pdf_report.pdf")
                else:
                    st.error("Mail not valid.")


def send_mail(mail: str, report_file: str):
    with open(report_file, "rb") as f:
        data = f.read()

    encoded_file = base64.b64encode(data).decode()

    api_key = os.getenv("MJ_APIKEY_PUBLIC", "notvalid")
    api_secret = os.getenv("MJ_APIKEY_PRIVATE", "notvalid")
    mailjet = Client(auth=(api_key, api_secret))
    data = {
        "FromEmail": os.getenv("MAIL", "notvalid@example.com"),
        "FromName": "Covid 19 App",
        "Subject": "Here you have your report!",
        "Text-part": "Hello, here is your report.",
        "Recipients": [{"Email": mail}],
        "Attachments": [
            {
                "Content-type": "application/pdf",
                "Filename": "report.pdf",
                "content": encoded_file,
            }
        ],
    }
    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        st.success("Mail sent. Please check your Inbox.")
    else:
        st.warning("Mail cannot be sent.")
