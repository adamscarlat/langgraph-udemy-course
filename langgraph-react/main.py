from dotenv import load_dotenv
load_dotenv()

from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph

from nodes import execute_tools, run_agent_reasoning
from state import AgentState

AGENT_REASON = "agent_reason"
ACT = "act"

def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT

flow = StateGraph(AgentState)
flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, execute_tools)

flow.add_conditional_edges(
    AGENT_REASON,
    should_continue
)

flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    print ("ReAct with LangGraph")
    res = app.invoke(
        input={
            "input": "What's the weather in San-Fransisco? First, write it and then triple it"
        }
    )
    print (res["agent_outcome"].return_values["output"])