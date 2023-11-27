import asyncio
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers.openai_functions import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv; load_dotenv()
import logging
from base import BaseConfig

config = BaseConfig(__name__)

class MyStreamingCallbackHandler(BaseCallbackHandler):
    """A basic Call Back Handler that will yield each new token"""

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        yield token

# llm = ChatOpenAI(temperature=0, model="gpt-4", streaming=True, callbacks=[MyStreamingCallbackHandler()])
llm = ChatOpenAI(temperature=0, model="gpt-4", streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
# llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

search = config.get_search_client()

tools = [
    Tool(
        name="search",
        func=search.run,
        description="useful for when you need to search the web for answers.",
    )]

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_functions(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

async def process_input(input_text):
    input_dict = {"input": input_text}
    async for chunk in agent_executor.astream(input_dict):
        # Process the streaming output chunk
        print(chunk)

# Define a function to run the asynchronous process_input function
def run_process_input(input_text):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_input(input_text))



async def aprocess_input(input_text):
    print("aprocess_input called")  # Add this line
    logging.info("aprocess_input called")  # Add this line
    input_dict = {"input": input_text}
    all_content = ""
    print("Calling agent_executor.astream(input_dict)")  # Add this line
    logging.info("Calling agent_executor.astream(input_dict)")  # Add this line
    async for chunk in agent_executor.astream(input_dict):
        logging.info(f"Received chunk: {chunk}")
        if isinstance(chunk, dict) and 'input' in chunk and 'output' in chunk:
            continue
        if chunk:
            all_content += chunk
        logging.info(f"Yielding all content: {all_content}")
        yield all_content

def arun_process_input(input_text):
    async def run():
        async for chunk in aprocess_input(input_text):
            print(chunk)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

# # Example usage
# input_text = "who is the president of the united states?"
# arun_process_input(input_text)