import streamlit as st
import pandas as pd
import duckdb
import io

csv = '''
beverage,price
orange juice,2.5
expresso,2
tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))
csv2 = '''
food item,food price
cookie,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = '''
SELECT * FROM beverages 
CROSS JOIN food_items'''
solution = duckdb.sql(answer).df()

st.write("Spaced Repetition System SQL practice")
with st.sidebar: #les mots-clés with sont des contexts manager
    option = st.selectbox("What would you like to review?",
                          ['Joins', 'GroupBy', 'WindowsFunctions'],
                          index=None,
                          placeholder="Choose a theme...")

    st.write(f'You selected: {option}')

st.header('Enter your code :')
query = st.text_area(label="Votre code sql ici", key='user_input')
if query:
    result = duckdb.query(query).df()
    st.dataframe(result)

tab2, tab3 = st.tabs(['Tables', 'Solution'])
with tab2:
    st.write('Table : beverages')
    st.dataframe(beverages)
    st.write('Table : food_items')
    st.dataframe(food_items)
    st.write('Expected')
    st.dataframe(solution)
with tab3:
    st.write(answer)


