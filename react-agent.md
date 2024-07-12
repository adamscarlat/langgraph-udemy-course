ReAct Agent Executor
--------------------
* (Background) - Chain of Thought prompting
  - CoT is a prompting technique in which the LLM is asked to answer while "thinking out loud"
  - For example,
    * Human input: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has
      3 tennis balls. How many tennis balls he has now?
    * Answer: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls.
      5 + 6 = 11. The answer is 11.
  - CoT improves the LLMs reasoning capabilities while also allowing us to debug.
    * We can see where the LLM stumbles when asked to provide an answer to a multi step problem.
  - CoT is especially powerful in solving math, reasoning and common sense problems
  - Example CoT prompt:

  ```md
  You are a highly intelligent and logical assistant capable of detailed and coherent reasoning. When presented with a problem, you will break it down into a series of logical steps and explain your thought process clearly and systematically. This approach is called "chain-of-thought reasoning."

  Here’s an example of how you should approach a problem using chain-of-thought reasoning:

  **Example Problem:**
  If a train travels 60 miles in 1.5 hours, what is its average speed?

  **Chain-of-Thought Reasoning:**
  1. **Understand the problem**: We need to find the average speed of a train that travels 60 miles in 1.5 hours.
  2. **Identify the formula**: The formula for average speed is total distance divided by total time.
  3. **Calculate the total distance**: The train travels 60 miles.
  4. **Calculate the total time**: The train travels for 1.5 hours.
  5. **Apply the formula**: Average speed = Total distance / Total time.
  6. **Compute the result**: Average speed = 60 miles / 1.5 hours.
  7. **Simplify the computation**: 60 divided by 1.5 equals 40.
  8. **State the final answer**: The average speed of the train is 40 miles per hour.

  When you are given a new problem, you should follow a similar chain-of-thought reasoning process. Ensure each step is clear and logically follows from the previous one. Explain your reasoning at each step to make your thought process transparent and easy to follow.

  **New Problem:**
  [Insert new problem here]
  ```

* The React agent pattern allows a model to apply reasoning and decide wether it should activate available tools.
  - It's shown to perform better than "chain-of-thought" prompting.
  - CoT lacks the ability to access real world information to improve its answers.

* How does it work?
  - Similar to CoT, ReAct also generates a type of CoT. Instead of just outputting thoughts, it also outputs actions and observations.
  - Example:
    * Human input: Which program was originally designed to interact with Apple Remote?
    * AI chain:
      - Thought 1: I need to search Apple Remote and find the program it was originally designed to
        interact with.
      - Act 1: search [Apple Remote]
      - Obs 1: The Apple Remote control was introduced in ....
      - Thought 2: (... makes conclusion from obs 1 ...)
      - Act 2: (... adjusts search parameters to get new information needed ...)
      - Obs 2: (... makes a new observation from all the sources it got ...)
      - ...

* Example ReAct prompt:

  ```md
  You are an intelligent assistant equipped with the ability to interact with various tools and APIs to accomplish tasks. You will follow a systematic approach to solve problems, react to the information you receive, and perform actions accordingly. 

  Here’s how you should approach tasks:

  1. **Understand the task**: Break down the task into clear and manageable steps.
  2. **Select the appropriate tool or API**: Determine which tool or API is needed to accomplish each step.
  3. **Execute actions using the tool or API**: Perform the required actions by interacting with the tool or API.
  4. **Interpret the results**: Analyze the results returned by the tool or API and decide the next steps.
  5. **React and iterate**: Based on the results, either proceed to the next step or refine your approach if necessary.
  6. **Provide a clear and detailed response**: Summarize the steps taken and the final outcome of the task.

  ### Example Scenario:

  **Task:** Retrieve the current weather for New York City.

  **Step-by-Step Approach:**
  1. **Understand the task**: We need to get the current weather information for New York City.
  2. **Select the appropriate tool or API**: Use a weather API to get the current weather information.
  3. **Execute actions using the tool or API**: Send a request to the weather API with "New York City" as the query.
  4. **Interpret the results**: Analyze the weather data returned by the API.
  5. **React and iterate**: If the data is incomplete or an error occurs, handle the error and retry.
  6. **Provide a clear and detailed response**: Summarize the weather information for New York City.

  ### New Task:

  [Insert new task here]

  ```
