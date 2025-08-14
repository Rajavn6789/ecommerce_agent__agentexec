from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv


from tools.sql import run_query_tool, list_tables, describe_tables, describe_tables_tool

load_dotenv()

#llm
llm = ChatOpenAI()

#prompt
tables = list_tables()

table_list = [t.strip() for t in tables.split(",")]
print(describe_tables(table_list))

system_msg = SystemMessage(content=f"""
You are an AI assistant with access to an SQLite database via tools.
Available Tables:
{tables}

Rules of Engagement:
1. For searches involving a city, state, pincode, or any place name, never assume column names.
   Always check the schema first by using: {describe_tables(['addresses'])} 
   but do this **only once** per session and reuse the cached schema for subsequent queries.
2. Read-only by default. Do not perform INSERT/UPDATE/DELETE/DDL unless user explicitly asks and confirms.
""")


print(system_msg.content)


human_msg = HumanMessagePromptTemplate.from_template("{input}")
prompt = ChatPromptTemplate(
    messages=[
        system_msg,
        human_msg,
        MessagesPlaceholder(variable_name="agent_scratchpad"),  
    ]
)

# Agent - chain that knows how to use tools
tools = [run_query_tool, describe_tables_tool]
agent = OpenAIFunctionsAgent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

# AgentExecutor - takes an agent and runs until the response is not functon call
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)


agent_executor("How many users are in the database?")
agent_executor("How many users have provided shipping address?")
agent_executor("Total number of products")

agent_executor("name of the user whose address contains Matthewport")
agent_executor("name of the user whose zipcode is 82596")
agent_executor("name of the user whose city contains East Jamesstad")
agent_executor("name of the user whose address contains Harrison Gardens")
agent_executor("name of the user whose state is FL")