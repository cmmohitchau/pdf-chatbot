import os
import uuid
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.retrievers import BM25Retriever

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("pdf-chatbot")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
bm25_retriever = None
all_documents = []

def vector_store(documents , source) -> bool:
    global bm25_retriever
    global all_documents

    try:
        # Unique IDs per upload to avoid overwriting previous docs
        upload_id = uuid.uuid4().hex[:8]
        ids = [
            f"{upload_id}-chunk-{i}" for i in range(len(documents))
            ]
        for i , doc in enumerate(documents):
            doc.metadata["document_name"] = source
            doc.metadata["vector_id"] = ids[i]
            doc.metadata["upload_id"] = upload_id
        vectorstore.add_documents(ids=ids, documents=documents)

        all_documents.extend(documents)
        bm25_retriever = BM25Retriever.from_documents(all_documents)
        return True

    except Exception as e:
        print(f"Error creating vector store: {e}")
        return False