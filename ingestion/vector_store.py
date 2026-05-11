import os
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.retrievers import BM25Retriever
load_dotenv()


api_key = os.getenv("OPENROUTER_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("pdf-chatbot")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

vectorstore = PineconeVectorStore(
            index=index,
            embedding=embeddings,
        )

bm25_retriever = None

def vector_store(documents):
    print("Creating vector store...")
    print(f"chunk size : {len(documents)}")

    try:
        print("Adding documents to vector store...")
        ids = [f"chunk-{i}" for i in range(len(documents))]

        vectorstore.add_documents(ids=ids, documents=documents)
        
        print("Creating bm25 retriever...")
        bm25_retriever = BM25Retriever.from_documents(documents)
    
        print("Vector store created successfully.")
        return vectorstore
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None
    
    