# pylint disable=(missing-module-docstring)

import logging
import os

import duckdb
import streamlit as st


def compare_solutions(user_query: str) -> None:
    """
    Checks that the user's query is correct by :
    1. checking the columns
    2. checking the values
    :param user_query: a string containing the query inserted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[[solution_df.columns]]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        print("Des colonnes sont manquantes")
    n_lignes_diff = result.shape[0] - solution_df.shape[0]
    if n_lignes_diff != 0:
        st.write(f"Le nombre de lignes est incorrect : {n_lignes_diff}")


if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error('creating dir "data"')
    os.mkdir("data")

if "exercises-sql-tables.duckdb" not in os.listdir("data"):
    # subprocess.run(['sys.executable', 'init_db.py']) #plus quali
    exec(open("init_db.py").read())  # pylint disable=(exec-used)

con = duckdb.connect("data/exercises-sql-tables.duckdb", read_only=False)

st.write("Spaced Repetition System SQL practice")
with st.sidebar:  # les mots-clés with sont des contexts manager
    themes = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review?",
        themes["theme"].unique(),
        index=None,
        placeholder="Choose a theme...",
    )
    st.write(f"You selected: {theme}")
    if theme:
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercise_query = "SELECT * FROM memory_state"

    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values(by="last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code :")
query = st.text_area(label="Votre code sql ici", key="user_input")

if query:
    compare_solutions(query)

tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:
    exercise_tables = exercise.loc[
        0, "tables"
    ]  # permet de convertir la liste string en vraie liste Python

    for table in exercise_tables:
        st.write(f"Table : {table}")
        df_table = con.execute(f"SELECT * from {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)
