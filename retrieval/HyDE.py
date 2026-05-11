from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY"),
)

hyde_prompt = """
You are a helpful assistant that generates a detailed answer to the user's question.
Generate a scientific answer to the following question, providing in-depth explanations and relevant information:
Question: {query}

"""
def hyde_fun(query):
    prompt = PromptTemplate.from_template(hyde_prompt)
    hyde_chain = prompt | llm
    response = hyde_chain.invoke({"query": query})
    return response

