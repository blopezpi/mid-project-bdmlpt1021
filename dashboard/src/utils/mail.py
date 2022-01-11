import base64
import os

import streamlit as st
from mailjet_rest import Client


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
