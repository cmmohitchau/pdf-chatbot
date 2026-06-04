import os
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder
from config.llm import llm

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    token=hf_token
)

def rerank(docs , query):
    if not docs:
        return []
    
    pairs = [ [query , doc.page_content] for doc in docs]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(docs , scores),
        key=lambda x : x[1],
        reverse=True
    )

    top_docs = [doc for doc, _ in ranked[:5]]
    
    return top_docs

def build_citations(docs):


    citations = {}

    for i, doc in enumerate(docs, start=1):
        citations[str(i)] = {
            "document_name": doc.metadata.get(
                "document_name",
                doc.metadata.get("source", "Unknown")
            ),
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
            "chunk_id": doc.metadata.get("chunk_id"),
            "chunk_index_in_page": doc.metadata.get(
                "chunk_index_in_page"
            ),
            "text": doc.page_content
        }
        print(f"Built citation for doc {i}: {citations[str(i)]} \n {'-'*40}")

    return citations

def build_context(docs):

    context_parts = []

    for i, doc in enumerate(docs, start=1):

        context_parts.append(
            f"""
            [CITATION_ID:{i}]
            DOCUMENT: {doc.metadata.get('source')}
            PAGE: {doc.metadata.get('page')}

            {doc.page_content}
            """
        )
    print(f"Built context with {len(context_parts)} parts")

    for part in context_parts:
        print(f"Context part:\n\n{part}\n\n{'-'*40}")

    return "\n\n".join(context_parts)

def compress(docs):

    citations = build_citations(docs)

    context = build_context(docs)

    return {
        "context": context,
        "citations": citations
    }