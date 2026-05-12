import os
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder
from config.llm import llm

load_dotenv()

hf_token = os.getenv("HF_TOKEN")
model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    token=hf_token
)

def rerank(docs , query):
    pairs = [ [query , doc.page_content] for doc in docs]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(docs , scores),
        key=lambda x : x[1],
        reverse=True
    )

    top_docs = [doc for doc, _ in ranked[:5]]
    
    return top_docs

def compress(docs, query):
    doc_texts = "\n\n".join([
        f"[Source: {doc.metadata.get('source', 'unknown')}, "
        f"Page: {doc.metadata.get('page', '?')}, "
        f"Chunk_id: {doc.metadata.get('chunk_id', '?')}]\n{doc.page_content}"
        for doc in docs
    ])

    prompt = f"""Extract only information relevant to the query below.
    Do not hallucinate. Return concise, relevant text only.
    Use this citation format after every claim:
    [Source: filename.pdf, Page: 3, Chunk_id: 5]

    QUERY: {query}

    DOCUMENTS:
    {doc_texts}
    """
    result = llm.invoke(prompt)
    return result.content