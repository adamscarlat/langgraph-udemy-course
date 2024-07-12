from dotenv import load_dotenv
load_dotenv()

from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from graph.chains.generation import generation_chain
from ingestion import get_retriever
from pprint import pprint

def test_retrieval_grader_answer_yes() -> None:
    # Retrieve documents
    question = "agent memory"
    retriever = get_retriever("./chroma")
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content

    # Grade document
    res: GradeDocuments = retrieval_grader.invoke({
        "question": question, "document": doc_txt
    })

    # Assertion
    assert res.binary_score == "yes"

def test_retrieval_grader_answer_no() -> None:
    # Retrieve documents
    # This is a query that is purposefully not related to document's content
    question = "how to make pizza?"
    retriever = get_retriever("./chroma")
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content

    # Grade document
    res: GradeDocuments = retrieval_grader.invoke({
        "question": question, "document": doc_txt
    })

    # Assertion
    assert res.binary_score == "no"

def test_generation_chain() -> None:
    # Retrieve documents
    question = "agent memory"
    retriever = get_retriever("./chroma")
    docs = retriever.invoke(question)

    # Generate
    generation = generation_chain.invoke({"context": docs, "question": question})
    pprint(generation)

    assert generation is not None