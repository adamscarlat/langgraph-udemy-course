from dotenv import load_dotenv
from langgraph.prebuilt.tool_executor import ToolExecutor

from react import react_agent_runnable, tools
from state import AgentState

load_dotenv()

def run_agent_reasoning(state: AgentState):
    # This will work since the state has the "input" field which is what the agent's prompt expects (part of it)
    agent_outcome = react_agent_runnable.invoke(state)

    # Note that this will override the original agent_outcome in the state
    return {"agent_outcome": agent_outcome}


tool_executor = ToolExecutor(tools)

def execute_tools(state: AgentState):
    # Since this node always comes after the reasoning node, the agent_outcome will be populated
    agent_action = state["agent_outcome"]

    # The agent_action contains the tool to run and its arguments
    output = tool_executor.invoke(agent_action)

    # This will add to the state's intermediate_steps list
    return {"intermediate_steps": [(agent_action, str(output))]}