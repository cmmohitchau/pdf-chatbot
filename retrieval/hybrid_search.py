
import ingestion.vector_store as vs

from langchain_classic.retrievers.ensemble import EnsembleRetriever

def hybrid_search(hyde_answer, top_k=15 , sources=None):
    vector_retriever = vs.vectorstore.as_retriever(
        search_kwargs={
            "k": top_k,         
            "filter": {"source": {"$in": sources if sources else []}}  } 
        )

    retriever = None

    if vs.bm25_retriever is not None:
        retriever = EnsembleRetriever(retrievers=[vector_retriever, vs.bm25_retriever], weights=[0.7, 0.3])
    try:
        results = None
        if retriever is None:
            results = vector_retriever.invoke(hyde_answer.content)
        else:
            results = retriever.invoke(hyde_answer.content)
        return results
    except Exception as e:
        print(f"Error during hybrid search: {e}")
        return None

    

    
