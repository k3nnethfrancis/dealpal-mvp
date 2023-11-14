
from backend.modules.openai_config import get_openai_client
from backend.modules.chat import chat
from backend.base import ASSISTANT_ID, show_json

client = get_openai_client()
assistant = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
thread = client.beta.threads.create()

chat(
    client=client,
    assistant=assistant,
    thread=thread,
    functions='code_interpreter',
    debug=False # Set to True to print message threads for each message
    )

print('Chat session ended. Printing thread messages...')
show_json(thread)