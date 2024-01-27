import streamlit as st
import pandas as pd
import duckdb

st.write("Hello World!")
data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    sql_query = st.text_area(label="écris1")
    st.write(f"La requête : {sql_query}")
    result = duckdb.query(sql_query).df()
    st.dataframe(result)

with tab3:
    input_txt = st.text_area(label="écris3")
    st.write(input_txt)
