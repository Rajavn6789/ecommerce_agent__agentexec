import sqlite3
from langchain.tools import Tool
from typing import List
from pydantic.v1 import BaseModel


conn = sqlite3.connect("db.sqlite")


def list_tables():
    try:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        rows = c.fetchall()
        return ", ".join(name for (name,) in rows)
    finally:
        if c:
            c.close()


# 1. Run sqlite query
def run_sqlite_query(query):
    try:
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        return rows
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {str(err)}"
    finally:
        if c:
            c.close()

class RunQueryArgsSchema(BaseModel):
    query: str
    
run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)

# 2. Describe tables
def describe_tables(table_names):
    if not table_names:
        return ""
    c = conn.cursor()
    try:
        placeholders = ", ".join("?" for _ in table_names)
        rows = c.execute(
            f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({placeholders});",
            list(table_names),
        )
        result = "\n".join(name for (name,) in rows if name)
    finally:
        c.close()
    return result

class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of those tables",
    func=describe_tables,
    DescribeTablesArgsSchema=RunQueryArgsSchema
)
