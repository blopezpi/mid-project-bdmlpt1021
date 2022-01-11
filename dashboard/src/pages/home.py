import streamlit as st


def app():
    st.title("Covid 19")

    st.caption("Hello to my Covid 19 Dashboard")
    col1, col2, col3 = st.columns([2, 4, 2])

    col2.image(
        "https://gacetamedica.com/wp-content/uploads/2020/09/GettyImages-1203949841-scaled.jpg",
        use_column_width=True,
    )
