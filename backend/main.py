
import os
from backend.modules.openai_config import get_openai_client
from backend.modules.chat import chat
from backend.base import ASSISTANT_ID, show_json

client = get_openai_client()
assistant = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
thread = client.beta.threads.create()

# add files
FILE = os.path.join(os.getcwd(), 'backend', 'data', 'alpha_creators.csv')
# Upload the file
file = client.files.create(
    file=open(FILE, "rb"),
    purpose="assistants",
)

# Update the assistant
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    # tools=[{"type": "code_interpreter"}],
    file_ids=[file.id],
)

chat(
    client=client,
    assistant=assistant,
    thread=thread,
    tools=['code_interpreter', 'search_tool'],
    debug=False # Set to True to print message threads for each message
)

print('Chat session ended. Printing thread messages...')
show_json(thread)