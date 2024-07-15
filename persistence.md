Persistence in LangGraph
------------------------
* Persistence in langgraph means that we can store our state in persistent storage and load it when we need to.

* Persistence in langgraph allows for "human in the loop"
  - We can define points where a human needs to supply input before continuing.
  - The graph is stopped and persisted. After a human provides input, the graph gets loaded again and continued.

* Persistence allows for better debugging.

The Checkpointer
----------------
* The Checkpointer is a persistence layer abstraction that langggraph offers.

* Langchain has many db integrations

* To add persistence to a graph, when we compile it we need to specify the checkpointer object:

```python
memory = SqliteSaver.from_conn_string(":checkpoints.sqlite:")
graph = workflow.compile(checkpointer=memory)
```
- When providing a checkpointer, langgraph stores the state at every step.