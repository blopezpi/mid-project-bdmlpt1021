import streamlit as st


class MultiApp:
    def __init__(self):
        self.pages = []

    def add_pages(self, title, func):
        self.pages.append({"title": title, "function": func})

    def run(self):
        pages = st.selectbox(
            "Navigation", self.pages, format_func=lambda page: page["title"]
        )

        pages["function"]()
