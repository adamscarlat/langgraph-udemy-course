Advanced RAG Architecture
-------------------------
* Based on 3 papers:
  - Self RAG
  - Adaptive RAG
  - Corrective RAG

* The general idea of these papers is to add reflection into our workflow
  - We reflect on the documents we received and curate them
  - We also reflect on the answer

* In addition, there is a routing element which routes the query to the correct data store where the correct
  answer might be.

Corrective RAG
--------------
* Provides higher quality answers for RAG

* We start in the same way to a regular RAG:
  - Get the user input, embed it
  - Find relevant documents from the vector store by semantic similarity

* Once we have the documents, we start to self reflect
  - Are the documents relevant to the query?
  - If yes, proceed with the RAG workflow
  - If not, filter those documents out and do a search online to augment the documents

Self RAG
--------
* With self RAG, we add another reflection step on the answer that the LLM generated. 
  - First we check if the answer contains hallucinations (meaning that it's not grounded in the documents)
    * If yes, we send the answer to the LLM again and ask it to correct it.
  - Next we check if the answer answered the original question
    * If no, we ask for another web search and generate a new answer