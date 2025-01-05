import ast
import json

from langchain.agents import AgentExecutor, tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

import getpass
import os

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, api_key=OPENAI_API_KEY)

@tool
def verify_api(curl_req: str) -> bool:
    """Verifies the API"""
    print("verifying the api")
    print(curl_req)
    return true

@tool
def log_api(curl_req: str) -> bool:
    """Logs the api"""
    print("logs the api")
    print(curl_req)
    return false

def get_crust_data_docs() -> str:
    """Returns the markdown version of docs"""
    with open('crustDataDE.md', 'r') as file:
        deContent = file.read()
    
    with open('crustDataAPI.md', 'r') as file:
        apiContent = file.read()
    
    return (deContent + apiContent).replace("{", "{{").replace("}", "}}")


system_prompt = f"""\
Role: You are an expert on CrustData's APIs, providing precise and professional guidance on their usage. \
Users approach you with questions related to CrustData’s API functionalities. \
You have access to comprehensive documentation on CrustData's API and are expected to respond using that information.

CrustData API Documentation:
{get_crust_data_docs()}

Steps to Follow:

Understand the user's query to identify the relevant information.
Provide a response detailing the necessary API endpoints, payload examples, and links to relevant resources (such as possible parameter values) whenever applicable.
If the answer is unclear or unavailable, acknowledge the uncertainty without guessing.
Avoid speculating on parameter values—refer users to accurate sources where possible.
Conversation Style:

Maintain a professional tone, adhering to the Blazon style of communication.
Example Query and Response:

Q: How do I search for people based on their current title, company, and location?

A: You can use the api.crustdata.com/screener/person/search endpoint. Below is an example curl request to search for people with the title "Engineer" at OpenAI in San Francisco:

bash
Copy code
curl --location 'https://api.crustdata.com/screener/person/search' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token $token' \
--data '<Relevant data>'
"""

# print(system_prompt)

MEMORY_KEY = "chat_history"
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt
,
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


tools = [verify_api, log_api]

llm_with_tools = llm.bind_tools(tools)


agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def get_chat_response(message: str, chat_history: list) -> str:
    print(chat_history)
    chat_history_messages = [
        AIMessage(content=chat_message['message']) 
        if chat_message['message_from'] == "AI" 
        else HumanMessage(content=chat_message['message'])
        for chat_message in chat_history
    ]
    
    result = agent_executor.invoke(
        {"input": message, "chat_history": chat_history_messages}
    )
    return result["output"]

# question = "How do I search for people given their current title, current company and location?"
# get_chat_response(question, [])
