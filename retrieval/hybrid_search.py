
from ingestion.vector_store import (
    vectorstore,
    bm25_retriever
)
from langchain_classic.retrievers.ensemble import EnsembleRetriever

def hybrid_search(hyde_answer, top_k=5):
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    retriever = None

    if bm25_retriever is not None:
        retriever = EnsembleRetriever(retrievers=[vector_retriever, bm25_retriever], weights=[0.7, 0.3])
    print("Performing hybrid search...")
    try:
        results = None
        if retriever is None:
            results = vector_retriever.invoke(hyde_answer.content)
        else:
            results = retriever.invoke(hyde_answer.content)
        print(f"Retrieved {len(results)} documents.")
        return results
    except Exception as e:
        print(f"Error during hybrid search: {e}")
        return None

    

    
