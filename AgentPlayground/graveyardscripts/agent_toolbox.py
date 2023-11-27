from backend.base import BaseConfig
from langchain.llms.openai import OpenAI
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.agents import tool

config = BaseConfig(__name__)


# tool boilerplate
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def run_search_tool(query: str) -> str:
    """
    Descr: Runs a research job to find answers to any query using the internet.
    Args:
        query: str
    Returns:
        answer: str
    """
    search = config.get_search_client()
    llm = OpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=0
        )
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    self_ask_with_search = initialize_agent(
        tools,
        llm, 
        agent=AgentType.SELF_ASK_WITH_SEARCH,
        verbose=True
    )
    return self_ask_with_search.run(query)
