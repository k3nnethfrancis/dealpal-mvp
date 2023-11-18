from backend.toolkit.function_jsons import function_json
from backend.base import BaseConfig

config = BaseConfig(__name__)

@config._async_logger
async def handle_upload_file(file, client, assistant_id):
    # Read the file
    contents = await file.read()

    # Upload the file to OpenAI
    uploaded_file = await client.files.create(
        file=contents,
        purpose="assistants",
    )
    # Update the assistant
    assistant = await client.beta.assistants.update(
        assistant_id=assistant_id,
        tools=[
            {"type": "code_interpreter"},
            {"type": "function", "function": function_json["search_tool"]},
            {"type": "function", "function": function_json["scraper_tool"]}
        ], # need to fix this tool assignment
        file_ids=[uploaded_file.id],
    )

    return {"filename": file.filename}