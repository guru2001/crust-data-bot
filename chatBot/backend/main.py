from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import get_chat_response
app = FastAPI()

chat_history = [{"message_from": "AI", "message": "Hello! How can I assist you today?"}]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class UserInput(BaseModel):
    text: str

@app.post("/apidocs")
async def process_input(user_input: UserInput):
    chat_history.append({"message_from": "Human", "message": user_input.text})
    response = get_chat_response(user_input.text, chat_history)
    chat_history.append({"message_from": "AI", "message": response})
    print("Message Response")
    return {"message": response}
