from typing import List, TypedDict
from langchain.schema import Document

class GraphState(TypedDict):
    """
    Represent the state of our graph

    Attributes:
        question: original user query
        generation: LLM generation
        web_search: whether to search online or now
        documents: list of documents
    """

    question: str
    generation: str
    web_search: bool
    documents: List[Document]