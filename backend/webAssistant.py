
from langchain_experimental.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import AgentExecutor
from langchain.schema.agent import AgentFinish
from langchain.tools import E2BDataAnalysisTool


tools = [E2BDataAnalysisTool(api_key="...")]
agent = OpenAIAssistantRunnable.create_assistant(
    name="langchain assistant e2b tool",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=tools,
    model="gpt-4-1106-preview",
    as_agent=True
)

def execute_agent(agent, tools, input):
    tool_map = {tool.name: tool for tool in tools}
    response = agent.invoke(input)
    while not isinstance(response, AgentFinish):
        tool_outputs = []
        for action in response:
            tool_output = tool_map[action.tool].invoke(action.tool_input)
            tool_outputs.append({"output": tool_output, "tool_call_id": action.tool_call_id})
        response = agent.invoke(
            {
                "tool_outputs": tool_outputs,
                "run_id": action.run_id,
                "thread_id": action.thread_id
            }
        )

    return response

response = execute_agent(agent, tools, {"content": "What's 10 - 4 raised to the 2.7"})
next_response = execute_agent(agent, tools, {"content": "now add 17.241", "thread_id": response.thread_id})
