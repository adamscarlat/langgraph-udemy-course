from typing import Any, Dict

from graph.chains.generation import generation_chain
from graph.state import GraphState

def generate(state: GraphState) -> Dict[str, Any]:
    print ("---GENERATE---")

    documents = state["documents"]
    question = state["question"]

    answer = generation_chain.invoke({
        "context": documents,
        "question": question
    })

    return {
        "documents": documents,
        "question": question,
        "generation": answer
    }