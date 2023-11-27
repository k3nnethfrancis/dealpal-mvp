import yaml
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, WebSocket
from base import BaseConfig
# from backend.modules.utils import show_json, get_agent_config
from agent_testing import Agent

config = BaseConfig(__name__)
# agent_config = get_agent_config('ari')
# assistant_id = agent_config.get('ID')

# Initialize FastAPI app
app = FastAPI()

# # CORS Middleware Setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# Initialize the chat agent
agent = Agent(tools=['search'], streaming=True)
chat = agent.initialize_agent()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for response in chat.invoke(data):
            await websocket.send_text(response)
