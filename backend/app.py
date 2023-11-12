import io
import time
from typing import Optional
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Initialize OpenAI API client
client = OpenAI()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model for message
class Message(BaseModel):
    content: Optional[str] = None

# Function to get the last message from a thread
def get_last_message(thread_id):
    messages_response = client.beta.threads.messages.list(thread_id=thread_id)
    messages = messages_response.data
  
    for message in reversed(messages):
        if message.role == 'assistant':
            return " ".join(
                content.text.value for content in message.content if hasattr(content, 'text')
            ).strip()
  
    return ""  # Return an empty string if there is no assistant message

# Endpoint for conversation with the assistant
@app.post("/converse")
async def converse(message: Message, file: Optional[UploadFile] = None):
    # Instructions and tools for 'Ari' assistant
    instructions = """
    You are Ari, an AI talent management agent modeled after the great Ari Gold.
    You are friendly, helpful, witty, funny, and a bit snarky. You're always looking for the next big thing.
    You help human talent agents manage dealflow for their creators.
    In the code interpreter, you have access to a database file of creators and their information.
    You can use this file to make recommendations about creators in response to user queries.
    You also have access to a web search function that you can use to research information about creators, brands, and current events.
    User queries may request responses to RFPs, help with generating copy, or help researching brands.
    """
    toolkit = [{"type": "code_interpreter"}]

    file_id = None
    if file:
        # Read the file asynchronously
        contents = await file.read()
        # Upload the file to OpenAI
        uploaded_file = client.files.create(
            file=io.BytesIO(contents),
            purpose='assistants'
        )
        file_id = uploaded_file.id

    # Initialize 'Ari' assistant with or without the uploaded file
    assistant_params = {
        'name': "Ari",
        'instructions': instructions,
        'tools': toolkit,
        'model': "gpt-4-1106-preview",
        'file_ids': [file_id] if file_id else []
    }
    assistant = client.beta.assistants.create(**assistant_params)
    assistant_thread = client.beta.threads.create()

    # Create a user message
    client.beta.threads.messages.create(
        thread_id=assistant_thread.id,
        role="user",
        content=message.content
    )

    # Create a run instance
    run = client.beta.threads.runs.create(
        thread_id=assistant_thread.id,
        assistant_id=assistant.id,
    )

    # Wait for the run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=assistant_thread.id,
            run_id=run.id,
        )
        if run_status.status == 'completed':
            break
        time.sleep(1)  # Avoid hitting the API too frequently

    # Retrieve the last message from the assistant
    return {get_last_message(assistant_thread.id)}
