import yaml
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from backend.app.chat import handle_chat_with_assistant
from backend.app.models import ChatResponse, ChatRequest
from backend.app.upload import handle_upload_file
from backend.base import BaseConfig
from backend.modules.utils import show_json, get_agent_config

config = BaseConfig(__name__)
agent_config = get_agent_config('ari')
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
client = config.get_async_openai_client()  # Get the asynchronous client

# Initialize assistant and thread as None
assistant = None
thread = None

@app.on_event("startup")
@client._async_logger
async def startup_event():
    global assistant, thread
    assistant = await client.beta.assistants.retrieve(
        assistant_id=assistant_id
        )  # Replace with your assistant ID
    thread = await client.beta.threads.create()

@app.post("/chat", response_model=ChatResponse)
@client._async_logger
async def chat_with_assistant(
    request: ChatRequest, 
    background_tasks: BackgroundTasks
    ) -> ChatResponse:
    return await handle_chat_with_assistant(
        request, 
        background_tasks, 
        client, 
        thread, 
        assistant
        )

@app.post("/upload")
@client._async_logger
async def upload_file(
    file: UploadFile = File(...)
    ):
    return await handle_upload_file(
        file, 
        client, 
        assistant_id
        )


