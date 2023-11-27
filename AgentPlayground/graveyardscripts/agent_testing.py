from langchain.utilities import SearchApiAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from base import BaseConfig
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler

from langchain.agents.initialize import initialize_agent
from langchain.memory import ConversationBufferMemory
import asyncio


class Agent(BaseConfig):
    def __init__(self, tools=[], model="gpt-4", temperature=0, streaming=False, callbacks=[]):
        super().__init__(__name__)
        self.search = SearchApiAPIWrapper(searchapi_api_key=self.SEARCHAPI_API_KEY)
        self.tools = []
        self.get_tools(tools)
        self.callbacks = callbacks
        if streaming:
            # self.callbacks.append(FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=["Final", "Answer", ":"]))
            self.callbacks.append(StreamingStdOutCallbackHandler())
        self.llm = ChatOpenAI(
            temperature=temperature, 
            model=model,
            openai_api_key=self.OPENAI_API_KEY,
            streaming=streaming, callbacks=self.callbacks
        )
        self.chat_history = []

    def get_tools(self, tools=[]):
        """
        Get tools from the list of tools and add them to self.tools
        """
        search = self.search
        toolbox = [
            Tool(
                name="Search",
                func=search.run,
                description="Useful when you need to answer questions about current events. You should ask targeted questions."
            ),
        ]
        # loop through the tool names listed in tools and check if they are in the toolbox 
        # if so add them to self.tools
        for tool_name in tools:
            tool_found = False
            for t in toolbox:
                if t.name.lower() == tool_name.lower():
                    self.tools.append(t)
                    tool_found = True
                    break
            if not tool_found:
                print(f"Error: Tool '{tool_name}' not found.")
    
    def initialize_agent(self, agent_type=AgentType.OPENAI_FUNCTIONS, verbose=False):
        """
        Initialize the agent
        """
        agent_config = {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: self.format_chat_history(x["intermediate_steps"]),
            "chat_history": lambda x: self.chat_history
        }
        return initialize_agent(
            self.tools,
            self.llm,
            agent=agent_type,
            agent_config=agent_config,
            memory=ConversationBufferMemory(),  # Corrected line
            verbose=verbose
        )
    async def initialize_agent_async(self, agent_type=AgentType.OPENAI_FUNCTIONS, verbose=False):
        agent_config = {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: self.format_chat_history(x["intermediate_steps"]),
            "chat_history": lambda x: self.chat_history
        }
        return await initialize_agent(
            self.tools,
            self.llm,
            agent=agent_type,
            agent_config=agent_config,
            memory=ConversationBufferMemory(),
            verbose=verbose
        )
    

    

agent = Agent(tools=['search'], streaming=True)

def chat_loop(agent, num_loops=10):
    """
    Run the chat agent in a loop, asking for human input each time.

    Parameters:
    agent (Agent): The chat agent.
    num_loops (int): The number of times to run the loop. Default is 10.
    """
    chat = agent.initialize_agent()
    for _ in range(num_loops):
        human_input = input("\nHuman: ")
        print()
        chat.run(human_input)
        print()

# Use the function
# chat_loop(agent)