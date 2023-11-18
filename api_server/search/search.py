from backend.base import BaseConfig
from langchain.llms.openai import OpenAI
from langchain.agents import AgentType, Tool, initialize_agent
import langchain; langchain.debug=True

config = BaseConfig(__name__)

# @config._logger
def run_search_tool(query):
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
