from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import os
import yaml
from backend.modules.openai_config import get_openai_client
import time
import json

agent_config_path = r'backend/agents/ari.yaml'
with open(agent_config_path, 'r') as file:
    agent_config = yaml.safe_load(file)

    # Extract and log configuration details
    assistant_id = agent_config.get('ID')
    
# Initialize FastAPI app
app = FastAPI()

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request and response
class ChatRequest(BaseModel):
    user_message: str

class ChatResponse(BaseModel):
    bot_response: str

# Global variables to hold client, assistant, and thread information
client = get_openai_client()
assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)  # Replace with your assistant ID
thread = client.beta.threads.create()

# Function to handle assistant interaction
def handle_assistant_interaction(user_message: str, functions: Dict[str, callable]) -> str:
    # Add user message to thread
    thread_message = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=user_message,
    ) 

    # Other parts of your chat interaction logic...

    # Example return (replace with actual logic)
    return "Response from assistant"

@app.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest, background_tasks: BackgroundTasks) -> ChatResponse:
    try:
        # Extract user message from request
        user_message = request.user_message

        # Define functions dictionary (update as needed)
        functions = {
            'code_interpreter': lambda x: "dummy response"  # Placeholder function
        }

        # Handle the assistant interaction (use a background task if it's a long-running operation)
        bot_response = handle_assistant_interaction(user_message, functions)

        return ChatResponse(bot_response=bot_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the server with: python -m uvicorn backend.app:app --reload
