from typing import Any, Dict

from graph.state import GraphState
from ingestion import get_retriever

# This node retrieves the relevant documents from the vector store based on the user's query
def retrieve(state: GraphState) -> Dict[str, Any]:
    print ("---RETRIEVE---")
    question = state["question"]

    retriever = get_retriever("./chroma")
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
