from config.llm import llm
def generate(query , retrieved_docs):

    prompt = f"""
    You are an ai assistant.Given a query generate a concise and accurate answer based on this context only.
    Context : {retrieved_docs}

    Query : {query}

    If you don't know the answer say so. Don't hallucinate the query.
    """

    return llm.invoke(prompt)


