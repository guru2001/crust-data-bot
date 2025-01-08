from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import get_chat_response

from retrieval import retrieve_documents_from_db, add_document_to_db
import asyncio

app = FastAPI()
chat_history = {}
lock = asyncio.Lock()

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


