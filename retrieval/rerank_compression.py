from sentence_transformers import CrossEncoder
from config.llm import llm

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
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

def compress(docs , query):
    prompt = f"""
    Extract only information relevant to:
    QUERY: {query}

    DOCUMENT : {docs}

    Return concise relevant text only.
    """
    
    return llm.invoke(prompt)



    

