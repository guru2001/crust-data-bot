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

from retrieval import retrieve_documents_from_db

import os

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, api_key=OPENAI_API_KEY)

@tool
def verify_api(curl_req: str) -> bool:
    """Verifies the API"""
    print("verifying the api")
    print(curl_req)
    return "True"

def get_crust_data_docs() -> str:
    """Returns the markdown version of docs"""
    with open('output_summary.md', 'r') as file:
        deContent = file.read()
    
    # with open('crustDataAPI.md', 'r') as file:
    #     apiContent = file.read()
    
    return (deContent).replace("{", "{{").replace("}", "}}")


system_prompt = f"""\
Role: You are an expert on CrustData's APIs, providing precise and professional guidance on their usage. \
Users approach you with questions related to CrustData’s API functionalities. \
You have access to comprehensive documentation on CrustData's API and are expected to respond using that information.

CrustData API Documentation:
{get_crust_data_docs()}

Steps to Follow:

1. Understand the user's query to identify the relevant information.
2. Provide a response detailing the necessary API endpoints, payload examples, and links to relevant resources (such as possible parameter values) as much as possible.
3. Always return response to the question first to the user.
4. If the answer is unclear or unavailable, acknowledge the uncertainty without guessing.
5. Avoid speculating on parameter values—refer users to accurate sources where possible.
6. Before providing the final response to the user, you **must verify the API call** using the `verify_api` tool. 
7. After verification is true, The final response **must** contain the curl request and brief explanation.
  

Conversation Style:
Maintain a professional tone, adhering to the Blazon style of communication.
Example Query and Response:

Q: How do I search for people based on their current title, company, and location?

A: You can use the api.crustdata.com/screener/person/search endpoint. Below is an example curl request to search for people with the title "Engineer" at OpenAI in San Francisco:

bash
```
curl --location 'https://api.crustdata.com/screener/person/search' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token $token' \
--data '<Relevant data>'
```
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
        MessagesPlaceholder(variable_name="retrieved_docs"),
        MessagesPlaceholder(variable_name=MEMORY_KEY),        
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [verify_api]

llm_with_tools = llm.bind_tools(tools)


agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
        "retrieved_docs": lambda x: x["retrieved_docs"]
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def get_chat_response(message: str, chat_history: list) -> str:
    chat_history_messages = [
        AIMessage(content=chat_message['message']) 
        if chat_message['message_from'] == "AI" 
        else HumanMessage(content=chat_message['message'])
        for chat_message in chat_history
    ]
    retrieved_docs = retrieve_documents_from_db(message) 
    retrieved_docs_formatted = [
        {"role": "system", "content": doc[0] if doc else ""}
        for doc in retrieved_docs
    ]
    result = agent_executor.invoke(
        {"input": message, "chat_history": chat_history_messages, "retrieved_docs": retrieved_docs_formatted}
    )
    return result["output"]

# question = "How do I search for people given their current title, current company and location? Also can you verify it"
# get_chat_response(question, [])
# question = """
#  I tried using the screener/person/search API to compare against previous values this weekend. I am blocked on the filter values. It seems like there's a strict set of values for something like a region. Because of that if I pass in something that doesn't fully conform to the list of enums you support for that filter value, the API call fails. The location fields for us are not normalized so I can't make the calls.
# I tried search/enrichment by email but for many entities we have @gmails rather than business emails. Results are not the best.


# Is there a standard you're using for the region values? I get this wall of text back when I don't submit a proper region value but it's hard for me to know at a glance how I should format my input
# {
#    "non_field_errors": [
#        "No mapping found for REGION: San Francisco. Correct values are ['Aruba', 'Afghanistan', 'Angola', 'Anguilla', 'Åland Islands', 'Albania', 'Andorra', 'United States', 'United Kingdom', 'United Arab Emirates', 'United States Minor Outlying Islands', 'Argentina', 'Armenia', 'American Samoa', 'US Virgin Islands', 'Antarctica', 'French Polynesia', 'French Guiana', 'French Southern and Antarctic Lands', 'Antigua and Barbuda', 'Australia', 'Austria', 'Azerbaijan', 'Burundi', 'Belgium', 'Benin', 'Burkina Faso', 'Bangladesh', 'Bulgaria', 'Bahrain', 'The Bahamas', 'Bosnia and Herzegovina', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Saint Kitts and Nevis', 'Saint Helena, Ascension and Tristan da
# …

# """
# get_chat_response(question, [])
