from core import comparisons
import core.main_page as main_page
import streamlit as st

if __name__ == "__main__":

    page_name_to_funcs = {
        "Main Page": main_page.main_page,
        "Comparison": comparisons.comparisons,
    }

    page_routes = st.sidebar.selectbox(
        "Select Page", list(page_name_to_funcs.keys())
    )

    page_name_to_funcs[page_routes]()
