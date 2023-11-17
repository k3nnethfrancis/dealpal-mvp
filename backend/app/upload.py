from backend.function_jsons.function_jsons import function_json
import logging


async def handle_upload_file(file, client, assistant_id):
    # Read the file
    contents = await file.read()

    # Upload the file to OpenAI
    uploaded_file = await client.files.create(
        file=contents,
        purpose="assistants",
    )
    logging.info(f"Uploaded file: {uploaded_file.filename}")
    # Update the assistant
    assistant = await client.beta.assistants.update(
        assistant_id=assistant_id,
        tools=[
            {"type": "code_interpreter"},
            {"type": "function", "function": function_json},
        ],
        file_ids=[uploaded_file.id],
    )

    return {"filename": file.filename}