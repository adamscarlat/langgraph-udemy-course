Production Challenges
---------------------
* Long runtime
  - These graphs have sequences of calls to LLMs and it can take some time completing a query.
  - To improve performance, we can use a semantic cache which checks the query embedding against a cache
    using vector similarity and if there's a hit, it returns.

* Context window
  - The prompts to the LLMs become pretty big, especially when we start accumulating state and history.
  - Most LLMs can accept around 32K tokens

* Hallucinations
  - RAG is a common technique to reduce hallucinations because we ground the LLM to a certain knowledge base.

* Fine tuning
  - Fine tuning an LLM for tool selection can help.

* Pricing
  - When running these agents in scale, it can become VERY expensive.
  - Semantic caching can help with this issue as well.

* Security
  - Since agents use tools, we're running a higher risk of security breach.
  - Using guardrails (e.g LLM Guard) can help 

* Overkilling
  - We shouldn't use LLM agents if we can achieve our goal using plain and deterministic code.