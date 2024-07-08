Introduction
------------
* LangGraph streamlines the building of agent based applications.

* Utilizes the concept of Flow Engineering

What is LangGraph?
------------------
* When we build an LLM powered application we start "losing control" over different aspects of the application:
  - The output of the LLM based components in the systems are at the discretion of the LLM.
  - The more we move towards an LLM based system, the less control we have. With agentic systems, we also give up control over:
    * The decisions of which steps to take next
    * The understandings of which steps are available 

* LangChain is a framework for building LLM applications. It has limitations when it comes to building complex agentic systems:
  - LangChain does not provide the ability to build cycles with larger amount freedom and more complex flows.
  - Langchain is great for direct workflows. Langgraph opens the door for more complex workflows.

Flow engineering
----------------
* Define how LLM powered apps define the program flow and sequence of operations.

* Flows are not necessarily linear. The LLM can generate multiple outputs that are checked individually.

* A structured process which guides the AI in improving the quality of its output.
  - Includes planning and testing 

* We as developers define the flow and we want the LLM to remain within the boundaries of the flow's scope.
  - Humans define the `what` and the LLM has autonomy over the `how`
* In the context of a state machine
  - We define the states and transitions
  - The LLM then runs it and decides which state to transition to based on the input.
  - For example, first state is "answer generation". After an answer is generated, the next states are to return the answer to the user OR to refine the answer. This is where the LLM makes the decision based on guidance in the form of prompts.

* Langgraph provides us with the abilities to combine agents into a state machine.
  - An agent is almost entirely autonomous. The trick is to combine these agents and LLMs into a flow.


LangGraph Components
--------------------
* With LangGraph we'll be implementing a well defined flow which leverages LLMs.

* LLMs may define in the flow: 
  - Which state we're going to go next
  - Run and complete tasks

* Core LangGraph components:
  - Nodes
    * Regular python functions
    * Always receive the graph state as input
    * Always returns an updated state
  - Edges
    * Connect the nodes. Can be defined conditionally and dynamically

* The start and end nodes
  - Entry and ending points to the graph
  - No ops

* The state
  - A dictionary which contains information that is important to the graph
  - For example, chat history, execution results, custom information
  - Any node can access it
  - Can be in-memory or persisted

* Cyclic graph
  - LangGraph allows for loops (very difficult to achieve with LangChain)

* Human in the loop
  - Allows for a human to "help" the LLM make the decision which node to 
    move to.

* Persistence
  - We can always persist the state of the graph to improve the user experience

