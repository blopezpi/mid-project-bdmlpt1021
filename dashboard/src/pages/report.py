import re

import streamlit as st
from config import user_pass
from utils.generate_pdf import generate_pdf
from utils.mail import send_mail
from utils.streamlit_utils import by_day_all, st_countries


def app():

    countries = st_countries()
    if countries:
        df = by_day_all(countries[:10])
        df.sort_values(by=["date"], inplace=True)
        df.drop(
            columns=[
                "recoveries_accumulated",
                "deaths_accumulated",
                "cases_accumulated",
            ],
            inplace=True,
        )
        generate_pdf(df)
        with open("pdf_report.pdf", "rb") as pdf:
            st.download_button("Download report", data=pdf, file_name="report.pdf")
        text_input_container = st.empty()
        password = text_input_container.text_input(
            "Enter a password to send you a mail with the report.", type="password"
        )
        if password == user_pass:
            text_input_container.empty()
            with st.form(key="mail_report"):
                mail = st.text_input(
                    "If you prefer you can get the report to your mail (Please provide us): "
                )
                if st.form_submit_button("Send by mail"):
                    if re.fullmatch(r"^[^@]+@[^@]+\.[^@]+$", mail):
                        send_mail(mail, "pdf_report.pdf")
                    else:
                        st.error("Mail not valid.")
