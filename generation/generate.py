from config.llm import llm
def generate(query, context):
    prompt = f"""Answer the question using ONLY the context below.
    You MUST include the citation tags exactly as they appear in the context after every claim.
    Do not drop or modify citation tags.

    Citation format: [Source: file.pdf, Page: 3, Chunk_id: 5]

    QUESTION: {query}

    CONTEXT:
    {context}

    ANSWER:"""
    result = llm.invoke(prompt)
    return result