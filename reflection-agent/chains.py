from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Prompt for the critic LLM
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's "
            "tweet. Always provide detailed recommendations, including requests for length, vitality, style, etc."
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

# Prompt taking a user's prompt and generating a tweet. It will
# revise it according to the state
generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts"
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

llm = ChatOpenAI()
generate_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
