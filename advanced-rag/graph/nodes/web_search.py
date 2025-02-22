from typing import Any, Dict

from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults

from graph.state import GraphState
from dotenv import load_dotenv
load_dotenv()

web_search_tool = TavilySearchResults(max_results=3)

def web_search(state: GraphState) -> Dict[str, Any]:
    print ("---WEB SEARCH---")

    question = state["question"]

    # Since we're post documents filtering, all documents in this list are curated and are relevant
    # to the user's query
    documents = state["documents"]

    tavily_results = web_search_tool.invoke({"query": question})

    # Combine web search results into a single document
    joined_tavily_result = "\n".join(
        [res["content"] for res in tavily_results]
    )
    web_results = Document(page_content=joined_tavily_result)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]

    return {"documents": documents, "question": question}


if __name__ == "__main__":
    web_search(state={"question": "agent memory", "documents": None})