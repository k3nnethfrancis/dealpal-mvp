import yaml
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from backend.app.chat import handle_chat_with_assistant
from backend.app.models import ChatResponse, ChatRequest
from backend.app.upload import handle_upload_file
from backend.modules.openai_config import get_async_openai_client

logging.basicConfig(level=logging.INFO)

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

# Global variables to hold client, assistant, and thread information
client = get_async_openai_client()  # Get the asynchronous client

# Initialize assistant and thread as None
assistant = None
thread = None

@app.on_event("startup")
async def startup_event():
    global assistant, thread
    assistant = await client.beta.assistants.retrieve(assistant_id=assistant_id)  # Replace with your assistant ID
    thread = await client.beta.threads.create()

@app.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest, background_tasks: BackgroundTasks) -> ChatResponse:
    return await handle_chat_with_assistant(request, background_tasks, client, thread, assistant)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await handle_upload_file(file, client, assistant_id)


