from dotenv import load_dotenv
load_dotenv(override=True)

from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader

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

def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print ("---CHECK HALLUCINATIONS---")

    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke({
        "documents": documents,
        "generation": generation
    })

    if hallucination_grade := score.binary_score:
        print ("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print ("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({
            "question": question,
            "generation": generation
        })
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESSES QUESTION---")
            return "not useful"
    else:
        print ("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS---")
        return "not supported"

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

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "useful": END,
        "not useful": WEBSEARCH,
        "not supported": GENERATE
    }
)

workflow.add_edge(WEBSEARCH, GENERATE)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
