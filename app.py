import streamlit as st
import core
import core.load_data
import core.transform_data as td

st.title("My First Streamlit App")
st.write("Hello, Streamlit")

st.dataframe(td.clean_data())