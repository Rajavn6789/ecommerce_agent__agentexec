from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool

load_dotenv()

#llm
llm = ChatOpenAI()

#prompt
tables = list_tables()
system_msg_1 = SystemMessage(content=f"you are an AI having access to SQLLite database \n {tables}")
system_msg_2 = SystemMessage(content=(
    "you are an AI having access to SQLLite database. \n"
    f"The database has tables of: {tables} \n"
    "Donot make any assumptions about what tables exist or what columns exist, "
    "Instead use the 'describe_tables' function"                                
))


human_msg = HumanMessagePromptTemplate.from_template("{input}")
prompt = ChatPromptTemplate(
    messages=[
        system_msg_2,
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