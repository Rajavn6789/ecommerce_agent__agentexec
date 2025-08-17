from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv


from tools.sql import run_query_tool, list_tables, describe_tables, describe_tables_tool
from tools.report import write_report_tool

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
human_msg = HumanMessagePromptTemplate.from_template("{input}")
chat_history_placeholder =  MessagesPlaceholder(variable_name="chat_history")
agent_scratchpad_placeholder = MessagesPlaceholder(variable_name="agent_scratchpad")
prompt = ChatPromptTemplate(
    messages=[
        system_msg,
        chat_history_placeholder, 
        human_msg,
        agent_scratchpad_placeholder,  
    ]
)

# Agent - chain that knows how to use tools
tools = [run_query_tool, describe_tables_tool, write_report_tool]
agent = OpenAIFunctionsAgent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)


# AgentExecutor - takes an agent and runs until the response is not functon call
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
)


# agent_executor("How many users are in the database?")
# agent_executor("How many users have provided shipping address?")
# agent_executor("Total number of products")
# agent_executor("name of the user whose address contains Matthewport")
# agent_executor("name of the user whose zipcode is 82596")
# agent_executor("name of the user whose city contains East Jamesstad")
# agent_executor("name of the user whose address contains Harrison Gardens")
# agent_executor("name of the user whose state is FL")
#agent_executor("Summarise the top 5 most popular products. Write the results to a report file in a table with product name, price and order count.")

agent_executor("How many orders are there? write the result to an html report")
agent_executor("repeat the exact same process for users.")