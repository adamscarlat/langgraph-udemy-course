from typing import List, Sequence, Literal

from dotenv import load_dotenv
from langgraph.constants import START

load_dotenv(override=True)

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from chains import generate_chain, reflection_chain

REFLECT = "reflect"
GENERATE = "generate"


# Once we get the response from the LLM, LangGraph will automatically add the response
# to the state.
def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})

# We send the generated tweet to the critic LLM. Before returning the response, we frame it
# as a HumanMessage. This is done to trick the generation LLM to take that feedback
# and treat it as a human prompt.
def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflection_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

# Define the graph structure - adding nodes
builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)

# A conditional edge to decide which state to go to.
def should_continue(state: List[BaseMessage]) -> Literal[REFLECT, END]:
    if len(state) > 2:
        return END
    return REFLECT

# Define the graph structure - adding edges
builder.add_edge(START, GENERATE)
builder.add_edge(REFLECT, GENERATE)
builder.add_edge(GENERATE, END)
builder.add_conditional_edges(
    GENERATE,
    should_continue,
)

# Take the printed mermaid syntax and paste it in mermaid.live to see the graph
# CAUTION: None of these show the conditional edges (even though they are set). This can be confusing...
graph = builder.compile()
print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

if __name__ == "__main__":
    inputs = HumanMessage(content="""
        Write a tweet about recent news events        
    """)
    # final_state: List[BaseMessage] = graph.invoke(inputs)
    # for msg in final_state:
    #     print(msg.type)
    #     print(msg.content)
    #     print("-" * 100)