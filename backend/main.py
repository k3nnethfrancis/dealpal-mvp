
import os
import yaml
from backend.modules.openai_config import get_openai_client
from backend.modules.chat import chat

client = get_openai_client()
assistant = client.beta.assistants.retrieve(assistant_id="asst_XLsEMqcFSAlcTvXMeMENg6x3")
thread = client.beta.threads.create()


chat(
    client=client,
    assistant=assistant,
    thread=thread,
    functions='code_interpreter'
    )

