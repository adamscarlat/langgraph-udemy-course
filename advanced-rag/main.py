from dotenv import load_dotenv
load_dotenv()

from graph.graph_builder import app

if __name__ == "__main__":
    print ("Advanced RAG")

    print (app.invoke(input={
        #"question": "What is agent memory?"
        "question": "How to make pizza?"
    }))