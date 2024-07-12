from typing import Any, Dict
from langchain.schema import Document

from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question.
    If any document is not relevant, we will set a flag to run a web search

    :param state: Current graph state
    :return: Filtered out irrelevant documents and updated web_search state
    """

    print ("---CHECK DOCUMENT RELEVANCE TO QUESTION---")

    question = state["question"]
    documents: list[Document] = state["documents"]

    # Relevant documents
    filtered_docs = []
    web_search = False

    # Filter out relevant documents and decide if a web search is needed
    for doc in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": doc.page_content}
        )
        grade = score.binary_score

        if grade.lower() == "yes":
            print ("---GRADE: FOUND RELEVANT DOCUMENT---")
            filtered_docs.append(doc)
        else:
            print ("---GRADE: FOUND A NONE RELEVANT DOCUMENT---")
            web_search = True
            continue

    return {
        "documents": filtered_docs,
        "question": question,
        "web_search": web_search
    }


