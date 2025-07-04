import io

import duckdb
import pandas as pd

con = duckdb.connect("data/exercises-sql-tables.duckdb", read_only=False)

data = {
    "theme": ["cross_joins", "cross_joins"],
    "exercise_name": ["beverages_and_food", "size_and_trademark"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
    "last_reviewed": ["1980-01-01", "1970-01-01"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")


CSV = """
beverage,price
orange juice,2.5
expresso,2
tea,3"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages as SELECT * from beverages")

CSV2 = """
food item,food price
cookie,2.5
chocolatine,2
muffin,3"""

food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items as SELECT * from food_items")

SIZES = """
size
XS
M
L
XL
"""
sizes = pd.read_csv(io.StringIO(SIZES))
con.execute("CREATE TABLE IF NOT EXISTS sizes as SELECT * from sizes")

TRADEMARKS = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademarks = pd.read_csv(io.StringIO(TRADEMARKS))
con.execute("CREATE TABLE IF NOT EXISTS trademarks as SELECT * from trademarks")

con.close()
