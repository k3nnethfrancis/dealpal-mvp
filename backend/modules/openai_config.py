from backend.modules.settings import Settings
from openai import OpenAI, AsyncOpenAI
from langchain.utilities import SearchApiAPIWrapper



def get_openai_client():
    settings = Settings()
    return OpenAI(api_key=settings.OPENAI_API_KEY)

def get_async_openai_client():
    settings = Settings()
    return AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Return the asynchronous client

def get_search_client():
    settings = Settings()
    return SearchApiAPIWrapper(api_key=settings.SEARCH_API_KEY)

