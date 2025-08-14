import sqlite3
from langchain.tools import Tool

conn = sqlite3.connect("db.sqlite")

def list_tables_lines():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(name for (name,) in rows)

def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return ", ".join(name for (name,) in rows)

def describe_tables(table_names):
    if not table_names:
        return ""
    c = conn.cursor()
    placeholders = ", ".join("?" for _ in table_names)
    rows = c.execute(
        f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({placeholders});",
        list(table_names),
    )
    return "\n".join(row[0] for row in rows if row and row[0])

def run_sqlite_query(query):
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {str(err)}"


# Tools: expose functions to an agent (LangChain Tool wrappers)
run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query",
    func=run_sqlite_query,
)

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of those tables",
    func=describe_tables,
)
