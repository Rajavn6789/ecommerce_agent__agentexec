from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool

load_dotenv()

#llm
llm = ChatOpenAI()

#prompt
human_msg = HumanMessagePromptTemplate.from_template("{input}")
prompt = ChatPromptTemplate(
    messages=[
        human_msg,
        MessagesPlaceholder(variable_name="agent_scratchpad"),  
    ]
)

# Agent
agent = OpenAIFunctionsAgent(
    llm=llm,
    prompt=prompt,
    tools=[run_query_tool],
)

# AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[run_query_tool],
    verbose=True,
    handle_parsing_errors=True,
)


agent_executor("How many users are in the database?")