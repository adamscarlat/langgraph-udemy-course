from dotenv import load_dotenv
load_dotenv(override=True)

from langgraph.graph import END, StateGraph

from graph.consts import RETRIEVE, GENERATE, GRADE_DOCUMENTS, WEBSEARCH
from graph.nodes import generate, grade_documents, retrieve, web_search
from graph.state import GraphState


def decide_to_generate(state):
    print ("---ASSESS GRADED DOCUMENTS---")

    if state["web_search"]:
        print ("---DECISION: NOT ALL DOCUMENTS ARE RELEVANT. GOING ONLINE---")
        return WEBSEARCH
    else:
        print ("---DECISION: ALL DOCUMENTS ARE RELEVANT. GENERATING---")
        return GENERATE

workflow = StateGraph(GraphState)
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    # There isn't really a need to use this here. It's only to show that it exists.
    # If the conditional edge is not returning node names, we can map whatever
    # it's returning to actual node names using this argument.
    {
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE
    }
)

workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
