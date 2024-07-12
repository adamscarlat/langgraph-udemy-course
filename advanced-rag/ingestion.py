from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings

load_dotenv()

sample_urls =[
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/"
]

def create_or_update_vectorstore(urls: list[str]):
    print ("Creating or updating the chroma vector store...")

    # Web based loader returns a list of documents for each URL
    docs = [WebBaseLoader(url).load() for url in urls]

    # We want to flatten that list of lists into a single list of documents
    docs_list = []
    for sublist in docs:
        for item in sublist:
            docs_list.append(item)

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    doc_split = text_splitter.split_documents(docs_list)

    # Create batches for chroma ingestion
    doc_split_batches = [doc_split[i:i+150] for i in range(0, len(doc_split), 150)]

    # Load the chunks into the Chroma DB vector store
    embedding=OpenAIEmbeddings()
    for batch in doc_split_batches:
        vectorstore = Chroma.from_documents(
            documents=batch,
            collection_name="rag-chroma",
            embedding=embedding,
            persist_directory="./chroma"
        )

    num_of_chunks_in_store = len(retriever.vectorstore.get()["documents"])
    print (f"Vector store update complete. Number of chunks in store: {num_of_chunks_in_store}")

def get_retriever(chroma_path: str, collection_name: str = "rag-chroma") -> VectorStoreRetriever:
    return Chroma(
        collection_name=collection_name,
        persist_directory=chroma_path,
        embedding_function=OpenAIEmbeddings()
    ).as_retriever()

if __name__ == "__main__":
    #create_or_update_vectorstore(sample_urls)

    retriever = get_retriever("./chroma")

    print(len(retriever.vectorstore.get()["documents"]))

