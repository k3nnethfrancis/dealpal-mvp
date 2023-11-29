from backend.toolkit.function_jsons import function_jsons
from backend.base import BaseConfig

config = BaseConfig(__name__)

@config._logger
async def handle_upload_file(file, client, assistant_id):
    # Read the file
    contents = await file.read()

    # Upload the file to OpenAI
    uploaded_file = await client.files.create(
        file=contents,
        purpose="assistants",
    )
    # Update the assistant
    ### NEED TO FIX: RIGHT NOT UPLOAD IS WHAT ASSIGNS TOOLS
    assistant = await client.beta.assistants.update(
        assistant_id=assistant_id,
        tools=[
            {"type": "code_interpreter"},
            {"type": "function", "function": function_jsons["search_tool"]},
            {"type": "function", "function": function_jsons["scraper_tool"]},
            {"type": "function", "function": function_jsons["email_sender_tool"]}
        ],
        file_ids=[uploaded_file.id],
    )

    return {"filename": file.filename}