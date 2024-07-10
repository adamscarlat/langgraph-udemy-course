import datetime

from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser
)

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from schemas import AnswerQuestion, ReviseAnswer

llm = ChatOpenAI(model="gpt-4-turbo-preview")

# Takes a tool calling, AIMessage and converts the tool call to a JSON structure which can be
# used as input to a tool
parser = JsonOutputToolsParser(return_id=True)

# Take the response from th LLM, search the function calling invocation and create an
# AnswerQuestion object from it. With a well-defined model (that has Fields with descriptions), this
# trick will GROUND the LLMs response to the appropriate format.
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])

# Prompt for the responder node. We'll reuse it across the different LLM calls (using the {first_instruction}).
# The actual input will be in the "messages" placeholder.
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",
         """
        You are an expert researcher. Current time: {time}
        
        1. {first_instruction}
        2. Reflect and critique your answer. Be severe to maximize improvement.
        3. Recommend search queries to research information and improve your answer. Always provide at least 
        1 search term.
        """
         ),
        MessagesPlaceholder("messages"),
        ("system", "Answer the user's question above using the required format.")
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat()
)

# First prompt - generates a vanilla answer to the user's query
first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer"
)

# Always use the AnswerQuestion tool to ground the answer to the model object.
# This will further guide the LLM on how to respond (using the model class's Fields and descriptions).
first_responder = first_responder_prompt_template | llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion"
)

revise_instructions = """
    Revise your previous answer using the new information. 
    - You should use the previous critique to add important information to your answer.
    - you MUST include numerous citations in your revised answer to ensure it can be verified.
    - Add a "References" section to the bottom of your answer (which does not count towards the word limit) 
      in the form of:
        - [1] https://example.com
        - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer to make sure it doesn't
      go over 250 words.
"""

# Second prompt - will use the first LLM answer and the search tool's results as input to revise the answer
# according to the instructions.
revisor = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")


if __name__ == "__main__":
    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous soc problem domain,"
        " list startups that do that and raised capital."
    )

    chain = (
        first_responder_prompt_template
        | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
        | parser_pydantic
    )

    res = chain.invoke(input={"messages": [human_message]})
    print (res)









