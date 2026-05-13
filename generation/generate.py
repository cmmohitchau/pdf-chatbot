from config.llm import llm

def generate(query, context):

    prompt = f"""
    You are a helpful AI assistant.

    Answer the user's question using ONLY the provided context.

    IMPORTANT RULES:
    1. Every factual claim MUST include its citation.
    2. Copy citations EXACTLY as provided.
    3. NEVER invent citations.
    4. NEVER modify citation formatting.
    5. If the context does not contain the answer, say:
    "I could not find enough information in the document."

    RESPONSE FORMAT:
    - Use clean markdown
    - Use short paragraphs
    - Use bullet points when helpful
    - Highlight important ideas using bold text
    - Make the answer easy to scan
    - Put citations at the end of sentences
    - DO NOT expose chunk ids unless they exist in citations
    - DO NOT mention "context" or "chunks"

    QUESTION:
    {query}

    CONTEXT:
    {context}

    ANSWER:
    """

    result = llm.invoke(prompt)
    return result