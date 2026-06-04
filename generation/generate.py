from config.llm import llm

def generate(query, context):

    prompt = f"""
    You are a retrieval QA system.

    You must answer ONLY from the supplied context.

    RULES:

    - Use only information found in the context.
    - Do not use prior knowledge.
    - Do not infer missing facts.
    - Do not guess.
    - Every factual sentence must contain citations.
    - Use only citation IDs that appear in the context.
    - If the answer is not explicitly present in the context,
    return exactly:
    I could not find enough information in the document.
    - Put the Citation IDs from the context at the end of every sentence of the claim like NoteBooklm.

    Every sentence MUST follow this pattern:

        <sentence>. [CITATION_ID:x]

        Example:

        John joined the company in 2020. [CITATION_ID:1]

        The company opened a new office in 2022. [CITATION_ID:2][CITATION_ID:3]

    

    CONTEXT START
    ================================
    {context}
    ================================
    CONTEXT END

    QUESTION:
    {query}

    Before answering, check:
    1. Is the answer explicitly contained in the context?
    2. Does every claim have a citation?

    If either check fails, return:

    I could not find enough information in the document.

    ANSWER:
    """

    result = llm.invoke(prompt)
    return result