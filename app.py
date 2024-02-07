# pylint disable=(missing-module-docstring)

import io

import duckdb
import pandas as pd
import streamlit as st
import ast

#ANSWER_STR = """
#SELECT * FROM beverages
#CROSS JOIN food_items"""
#solution = duckdb.sql(ANSWER_STR).df()

con = duckdb.connect('data/exercises-sql-tables.duckdb', read_only=False)

st.write("Spaced Repetition System SQL practice")
with st.sidebar:  # les mots-clés with sont des contexts manager
    theme = st.selectbox(
        "What would you like to review?",
        ["cross_joins", "GroupBy", "windows_functions"],
        index=None,
        placeholder="Choose a theme...",
    )
    st.write(f"You selected: {theme}")

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("Enter your code :")
query = st.text_area(label="Votre code sql ici", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)
#
#     try:
#         result = result[[solution.columns]]
#         st.dataframe(result.compare(solution))
#     except KeyError as e:
#         print("Des colonnes sont manquantes")
#
#     n_lignes_diff = result.shape[0] - solution.shape[0]
#     if n_lignes_diff != 0:
#         st.write(f"Le nombre de lignes est incorrect : {n_lignes_diff}")
#
#
tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"]) #permet de convertir la liste string en vraie liste Python
    for table in exercise_tables:
        st.write(f"Table : {table}")
        df_table = con.execute(f"SELECT * from {table}").df()
        st.dataframe(df_table)

with tab3:
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    st.write(answer)
