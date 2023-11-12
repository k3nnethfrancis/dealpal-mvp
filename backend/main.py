import time
import threading
import os
import openai
from openai import OpenAI
import dotenv; dotenv.load_dotenv()
import io
from time import sleep
from backend.tools import toolkit
from langchain.schema.agent import AgentFinish
from backend.base import (
    SERPER_API_KEY,
    SERPAPI_API_KEY,
    OPENAI_API_KEY,
    ASSISTANT_ID
)
from typing import Any


client = OpenAI()

def get_last_message(thread_id):
    messages_response = client.beta.threads.messages.list(thread_id=thread_id)
    messages = messages_response.data
  
    # Iterate through messages in reverse chronological order to find the last assistant message
    for message in reversed(messages):
        if message.role == 'assistant':
            message_content = " ".join(
                content.text.value for content in message.content if hasattr(content, 'text')
            )
            return message_content.strip()
  
    return ""  # Return an empty string if there is no assistant message

from typing import Any

class OpenAIAssistantRunnable:
    def __init__(self, assistant_id, name, instructions, tools, model, as_agent=False):
        self.assistant_id = assistant_id
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.as_agent = as_agent
        self.client = openai.OpenAI()

    @classmethod
    def create_assistant(cls, assistant_id, name, instructions, tools, model, as_agent=False):
        assistant = cls(assistant_id, name, instructions, tools, model, as_agent)
        return assistant

    def invoke(self, input):
        if "thread_id" in input:
            run = self.client.beta.threads.runs.create(input["thread_id"], assistant_id=self.assistant_id, **input)
        else:
            thread = self.client.beta.threads.create()
            message = self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=input["content"])
            run = self.client.beta.threads.runs.create(thread_id=thread.id, assistant_id=self.assistant_id)
        return self._get_response(run.id, run.thread_id)

    def _get_response(self, run_id: str, thread_id: str) -> Any:
        in_progress = True
        while in_progress:
            run = self.client.beta.threads.runs.retrieve(run_id, thread_id=thread_id)
            in_progress = run.status in ("in_progress", "queued")
            if in_progress:
                sleep(1)  # Wait for 1 second before checking the run status again
        return run

def execute_agent(agent, tools, input):
    tool_map = {tool.name: tool for tool in tools}
    response = agent.invoke(input)
    while not isinstance(response, AgentFinish):
        tool_outputs = []
        for action in response:
            tool_output = tool_map[action.tool].invoke(action.tool_input)
            tool_outputs.append({"output": tool_output, "tool_call_id": action.tool_call_id})
        response = agent.invoke(
            {
                "tool_outputs": tool_outputs,
                "run_id": action.run_id,
                "thread_id": action.thread_id
            }
        )

    return response

def converse(assistant_params, message_count, file_path=None):
    # If a file path is provided, read the file and add its content to assistant_params
    if file_path:
        file = client.files.create(
            file=open(file_path, 'rb'),
            purpose='assistants'
        )
        assistant_params['file_ids'] = [file.id]

    # Create the assistant
    assistant = OpenAIAssistantRunnable.create_assistant(
        # assistant_id=assistant_params['assistant_id'],
        name=assistant_params['name'],
        instructions=assistant_params['instructions'],
        tools=assistant_params['tools'],
        model=assistant_params['model'],
        as_agent=True
    )

    def conversation(start_message, assistant, msg_limit):
        message_content = start_message

        for i in range(msg_limit):
            if i != 0:  # Skip user input for the first message
                message_content = input("Your turn: ")

            # Execute the agent and handle tool outputs
            response = assistant.invoke({"content": message_content})
            if 'return_values' in response:
                message_content = response['return_values']['output']
            else:
                # Handle tool outputs here
                pass

            print(f"Assistant speaking... (Turn {i + 1})")
            if 'return_values' in response and 'output' in response['return_values']:
                print(response['return_values']['output']+"\n")

    # Start the conversation
    start_message = input("Start the conversation: ")
    conversation(start_message, assistant, message_count)

# Define the parameters for the two assistants (example parameters provided)
instructions = """
You are Ari, an AI talent management agent modeled after the great Ari Gold.
You are friendly, helpful, witty, funny, and a bit snarky. You're always looking for the next big thing.
You help human talent agents manage dealflow for their creators.
In the code interpreter, you have access to a database file of creators and their information.
You can use this file to make recommendations about creators in response to user queries.
You also have access to a web search function that you can use to research information about creators, brands, and current events.
User queries my request responses to RFPs, help with generating copy, or help reseaching brands."""


toolkit = [{
    "type": "code_interpreter"
    }]
assistant_params = {
    'assistant_id': ASSISTANT_ID,  # Replace with your actual assistant ID
    'name': "Ari",
    'instructions': instructions,
    'tools': toolkit,
    'model': "gpt-4-1106-preview"
}

# Example usage:a
converse(assistant_params, 5, file_path="/Users/kennycavanagh/Desktop/files/lab/repositories/Ari/backend/data/alpha_creators - Sheet1 copy.csv")