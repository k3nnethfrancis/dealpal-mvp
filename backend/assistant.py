
import openai
from dotenv import load_dotenv
import time
import os

load_dotenv()
client = openai.OpenAI()

FILE_PATH = "/Users/kennycavanagh/Desktop/files/lab/repositories/Ari/backend/data/alpha_creators - Sheet1 copy.csv"

file = client.files.create(
    file=open(FILE_PATH, "rb"),
    purpose='assistants'
)

instructions = """
You are Ari, an AI talent management agent modeled after the great Ari Gold.
You are friendly, helpful, witty, funny, and a bit snarky. You're always looking for the next big thing.
You help human talent agents manage dealflow for their creators.
In the code interpreter, you have access to a database file of creators and their information.
You can use this file to make recommendations about creators in response to user queries.
You also have access to a web search function that you can use to research information about creators, brands, and current events.
User queries my request responses to RFPs, help with generating copy, or help reseaching brands.
"""

toolkit = [{"type": "code_interpreter"}]

assistant_params = {
    'name': "Ari",
    'instructions': instructions,
    'tools': toolkit,
    'model': "gpt-4-1106-preview",
    'file_ids': [file.id]
}

assistant = client.beta.assistants.create(**assistant_params)

def print_full_thread(thread_id):
    messages_response = client.beta.threads.messages.list(thread_id=thread_id)
    for message in messages_response.data:
        role = "Assistant" if message.role == "assistant" else "User"
        content = " ".join([c.text.value for c in message.content if hasattr(c, 'text')])
        print(f"{role}: {content}")

def run_conversation(thread_id, assistant_id, max_messages=5):
    for _ in range(max_messages):
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            elif run_status.status == 'requires_action':
                # Handle required actions here (if any)
                pass
            time.sleep(1)

        print_full_thread(thread_id)  # Print the full thread after each exchange

thread = client.beta.threads.create()
run_conversation(thread.id, assistant.id)
