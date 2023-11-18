import logging
from fastapi import HTTPException, BackgroundTasks
from backend.app.models import ChatRequest, ChatResponse
from backend.app.handle_assistant_interactions import handle_assistant_interaction
from backend.base import BaseConfig

config = BaseConfig(__name__)

@config._logger
async def handle_chat_with_assistant(
        request: ChatRequest, 
        background_tasks: BackgroundTasks, 
        client, 
        thread, 
        assistant
        ) -> ChatResponse:
    try:
        user_message = request.user_message
        logging.info(f"Received user message: {user_message}")

        # Ensure client, thread, and assistant are not None
        if client is None or thread is None or assistant is None:
            raise ValueError("Client, thread, or assistant is not properly initialized.")

        bot_response = await handle_assistant_interaction(
            user_message, 
            client, 
            thread, 
            assistant
            )

        return ChatResponse(bot_response=bot_response)
    except HTTPException as http_exc:
        # Re-raise FastAPI HTTP exceptions without logging them as errors
        raise
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
