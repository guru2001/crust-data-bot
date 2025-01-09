from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import get_chat_response

from retrieval import retrieve_documents_from_db, add_document_to_db
import asyncio

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import os
app = FastAPI()
chat_history = {}
lock = asyncio.Lock()

ALLOWED_CHANNELS = ["C087ZM6PWJX"]
ALLOWED_USERS = ["U02VBVB9F28"]
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class UserInput(BaseModel):
    text: str
    threadId: str

@app.post("/apidocs")
async def process_input(user_input: UserInput):
    thread_id = user_input.threadId
    async with lock:
        if thread_id not in chat_history:
            chat_history[thread_id] = [{"message_from": "AI", "message": "Hello! How can I assist you today?"}]
        
        chat_history[thread_id].append({"message_from": "Human", "message": user_input.text})
        response = get_chat_response(user_input.text, chat_history[thread_id])
        chat_history[thread_id].append({"message_from": "AI", "message": response})
        try:
            document = 'Q:' + user_input.text + '\n A:' + response
            existing_results = retrieve_documents_from_db(document, 1)
            if existing_results['documents'] == [[]]:
                # print("here1")
                add_document_to_db(thread_id, document)
            elif existing_results['distances'][0][0] > 0.2:   # Similarity threshold
                # print("here2")
                add_document_to_db(thread_id, document)    
            else: 
                print("Present in db")
        except Exception as e:
            print("failed to add in vectordb", e)

    return {"message": response}

def post_to_slack(channel, text, thread_id):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text,
            thread_ts=thread_id
        )        
        print(f"Message sent to channel: {response['channel']}")
        print(f"Timestamp: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


def handle_slack_message_events(event):
    user = event.get("user")
    channel = event.get("channel")
    text = " ".join(event.get("text").split(" ")[1:])
    thread_id = event.get("event_ts")
    print(channel, user, text, thread_id)
    if channel in ALLOWED_CHANNELS:
        if thread_id not in chat_history:
            chat_history[thread_id] = [{"message_from": "AI", "message": "Hello! How can I assist you today?"}]

        chat_history[thread_id].append({"message_from": "Human", "message": text})

        response = get_chat_response(text, chat_history[thread_id])
        chat_history[thread_id].append({"message_from": "AI", "message": response})
        
        post_to_slack(channel, response, thread_id)

        try:
            document = f"Q: {text}\nA: {response}"
            existing_results = retrieve_documents_from_db(document, 1)
            if existing_results['documents'] == [[]] or existing_results['distances'][0][0] > 0.2:
                add_document_to_db(thread_id, document)
        except Exception as e:
            print("Failed to add in vectordb:", e)


@app.post("/slack/events")
def slack_events(req: dict, background_tasks: BackgroundTasks):
    if req["type"] == "url_verification":
        return { "challenge": req["challenge"] } 
    if req["event"]["type"] == "app_mention":
        print("start")
        # asyncio.create_task(handle_slack_message_events(req["event"]))
        background_tasks.add_task(handle_slack_message_events, req["event"])
        print("ending now")
        return {"status": "OK"}
