import os
import dotenv; dotenv.load_dotenv()

from langchain import hub
from langsmith import Client

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

from langchain.tools.render import format_tool_to_openai_function

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.llms import OpenAI

from backend.chatbot.agent_toolbox import run_search_tool

# langsmith client
langsmith_client = Client()

# llm model
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    streaming=True,
    callbacks=[FinalStreamingStdOutCallbackHandler()]
)

# tool list
tools = [run_search_tool]

# bind tools to openAI functions format
llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])


# Now let us create the prompt. 
#   Because OpenAI Function Calling is finetuned for tool usage, we hardly need any instructions on how to reason, or how to output format. 
#   We will just have two input variables: input and agent_scratchpad. input should be a string containing the user objective. 
#       agent_scratchpad should be a sequence of messages that contains the previous agent tool invocations and the corresponding tool outputs
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful web assistant, able to help users with their searches",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Putting those pieces together, we can now create the agent. We will import two last utility functions: 
#     a component for formatting intermediate steps (agent action, tool output pairs) to input messages 
#         that can be sent to the model, and a component for converting the output message into an agent action/agent finish
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

from langchain.schema.agent import AgentFinish
from langchain.schema.messages import AIMessage, HumanMessage
from langchain.schema.agent import AgentAction

class AgentIntermediateAnswer(AgentAction):
    def __init__(self, tool: str, tool_input: str, log: str):
        super().__init__(tool=tool, tool_input=tool_input, log=log)

from langchain.schema.messages import AIMessage
from langchain.schema.agent import AgentActionMessageLog


def chat_loop(user_input, agent, chat_log, step_history):
    # Enter the loop
    while True:
        # Create the input dictionary for the agent
        agent_input = {
            "input": user_input,
            "intermediate_steps": step_history,
        }

        # Invoke the agent
        output = agent.invoke(agent_input)

        # Check if the agent has finished
        if isinstance(output, AgentFinish):
            final_result = output.return_values["output"]
            chat_log.append(HumanMessage(content=user_input))
            chat_log.append(AIMessage(content=final_result))
            step_history.append((HumanMessage(content=user_input), AIMessage(content=final_result)))
            print(final_result)
            break

        # Check if the output is an intermediate answer
        if isinstance(output, AgentActionMessageLog):
            intermediate_answer = output.log
            step_history.append((output, intermediate_answer))
            continue

        # Print the tool name and input
        print(f"TOOL NAME: {output.tool}")
        print(f"TOOL INPUT: {output.tool_input}")

        # Execute the tool function
        tool = {"run_search_tool": run_search_tool}[output.tool]
        observation = tool.run(output.tool_input)

        # Update the chat history
        if isinstance(output, AgentAction):
            step_history.append((output, observation))

    # Return the final response
    return final_result

# Create empty chat history objects
chat_log = []
step_history = []

# Example usage
for _ in range(10):
    human_input = input("Enter your query: ")
    final_response = chat_loop(human_input,
                               agent, 
                               chat_log, 
                               step_history
                            )

    print('\n\nprinting response...\n')
    print(final_response)

    # print('\n\nprinting chat log...\n')
    # print(chat_log)

    # print('\n\nprinting step history...\n')
    # print(step_history)
