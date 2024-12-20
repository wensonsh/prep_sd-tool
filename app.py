import streamlit as st
import pandas as pd

st.write("Hello world")
st.text_input("This is a text field", key="text")
st.session_state.name

df = pd.DataFrame({
    "first column": [1, 2, 3],
    "second column": [4, 5, 6]
})
option = st.selectbox(
    "Select a number", df["first column"])
"You selected: ", option