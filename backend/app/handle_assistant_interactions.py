import time
import json
from backend.api_calls.api_calls import run_selenium

# Function to handle assistant interaction
async def handle_assistant_interaction(user_message: str, client, thread, assistant) -> str:
    # Add user message to thread
    thread_message = await client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=user_message,
    )

    # Get assistant response in thread
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for run to complete
    while True:
        time.sleep(1)

        run = await client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

        if run.status == "requires_action":
            # Extract single tool call
            tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            # Dynamically call the function with the given name and arguments
            response = globals().get(func_name)(*args) if globals().get(func_name) else None

            if response is None:
                raise ValueError(f"Function '{func_name}' not found or invalid arguments.")

            ## get back to the assistant
            run = await client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(response),
                    }
                ],
            )

        if run.status == "completed":
            break

    # Get most recent message from thread
    thread_messages = await client.beta.threads.messages.list(thread.id, limit=10, order='desc')

    # Get assistant response from message
    assistant_response = thread_messages.data[0].content[0].text.value

    return assistant_response
