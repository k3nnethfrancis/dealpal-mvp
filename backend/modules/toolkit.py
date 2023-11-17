from backend.modules.tool_config import get_search_client
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms.openai import OpenAI
import dotenv; dotenv.load_dotenv()
# import langchain; langchain.debug=True

def search_tool(query):

    search = get_search_client()
    llm = OpenAI(temperature=0)
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    self_ask_with_search = initialize_agent(
        tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
    )
    return self_ask_with_search.run(query)


# Define a dictionary mapping tool names to functions
tool_functions = {
    'search_tool': search_tool,
    # Add other tools here
}

# Define a dictionary mapping tool names to their JSON schemas
tool_jsons = {
    'search_tool': {
        "name": "search_tool",
        "description": "Searches for an answer using a sub-agent",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"],
        },
    },
    # Add other tools here
}

# sub_agent_search_tool("What are RFKs latest polling numbers (in the last week)?")
