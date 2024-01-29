# pylint disable=(missing-module-docstring)

import io

import pandas as pd
import streamlit as st
import duckdb

CSV = """
beverage,price
orange juice,2.5
expresso,2
tea,3"""
beverages = pd.read_csv(io.StringIO(CSV))
CSV2 = """
food item,food price
cookie,2.5
chocolatine,2
muffin,3"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages 
CROSS JOIN food_items"""
solution = duckdb.sql(ANSWER_STR).df()

st.write("Spaced Repetition System SQL practice")
with st.sidebar:  # les mots-clés with sont des contexts manager
    option = st.selectbox(
        "What would you like to review?",
        ["Joins", "GroupBy", "WindowsFunctions"],
        index=None,
        placeholder="Choose a theme...",
    )
    st.write(f"You selected: {option}")

st.header("Enter your code :")
query = st.text_area(label="Votre code sql ici", key="user_input")

if query:
    result = duckdb.query(query).df()
    st.dataframe(result)

    try:
        result = result[[solution.columns]]
        st.dataframe(result.compare(solution))
    except KeyError as e:
        print("Des colonnes sont manquantes")

    n_lignes_diff = result.shape[0] - solution.shape[0]
    if n_lignes_diff != 0:
        st.write(f"Le nombre de lignes est incorrect : {n_lignes_diff}")


tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:
    st.write("Table : beverages")
    st.dataframe(beverages)
    st.write("Table : food_items")
    st.dataframe(food_items)
    st.write("Expected")
    st.dataframe(solution)
with tab3:
    st.write(ANSWER_STR)
