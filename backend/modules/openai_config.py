from backend.modules.settings import Settings
from openai import OpenAI, AsyncOpenAI

def get_openai_client():
    settings = Settings()
    return OpenAI(api_key=settings.OPENAI_API_KEY)

def get_async_openai_client():
    settings = Settings()
    return AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Return the asynchronous client