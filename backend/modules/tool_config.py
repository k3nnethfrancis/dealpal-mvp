from backend.modules.settings import Settings
from langchain.utilities import SearchApiAPIWrapper

def get_search_client():
    settings = Settings()
    return SearchApiAPIWrapper(searchapi_api_key=settings.SEARCHAPI_API_KEY)

