import operator

from typing import Annotated, TypedDict, Union

from langchain_core.agents import AgentAction, AgentFinish


# Custom state for LangGraph
class AgentState(TypedDict):
    # Initial user input
    input: str

    # Agent output at the step: either to continue or finish
    agent_outcome: Union[AgentAction, AgentFinish, None]

    # Tells LangGraph to keep adding to this list the intermediate state
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
