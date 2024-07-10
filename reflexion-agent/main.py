from dotenv import load_dotenv
load_dotenv(override=True)

from typing import List
from pprint import  pprint

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph

from chains import revisor, first_responder
from tool_executor import execute_tools

# Iteration limits for the critique-revision loop
MAX_ITERATIONS = 2
builder = MessageGraph()
builder.add_node("draft", first_responder)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor)

builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")

# This will serve as a conditional edge to decide if to finish the graph
# execution or continue.
def event_loop(state: List[BaseMessage]) -> str:
    # We'll use the tool invocations as a counter for the iterations
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits

    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"

builder.add_conditional_edges("revise", event_loop)
builder.set_entry_point("draft")
graph = builder.compile()

print (graph.get_graph().draw_ascii())
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    print ("Graph execution")
    res: List[BaseMessage] = graph.invoke("Is it a good time to sell Bloom Energy stock? Specify recent events that"
                       "may affect the answer."
    )

    answer_json = res[-1].additional_kwargs["tool_calls"][0]["function"]["arguments"]
    pprint (answer_json)

