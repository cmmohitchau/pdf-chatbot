from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ingestion.load_documents import load_documents
from ingestion.split_document import split_document
from ingestion.vector_store import vector_store
from retrieval.hyde import hyde
from retrieval.hybrid_search import hybrid_search
from retrieval.rerank_compression import (rerank , compress)
from generation.generate import generate

app = FastAPI()

origins = [
   "http://localhost:3000",
   "https://myapp.com",
]


app.add_middleware(
CORSMiddleware,
allow_origins=origins, 
allow_credentials=True, 
allow_methods=["*"], 
allow_headers=["*"], 
)

ALLOWED_CONTENT_TYPES = {"application/pdf"}

@app.post("/upload")
async def upload(file: UploadFile):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    texts = load_documents(file)

    if texts is None:
        raise HTTPException(status_code=422, detail="Failed to extract text from PDF.")

    documents = split_document(texts , file.filename)
    if not documents:
        raise HTTPException(status_code=422, detail="Failed to split document into chunks.")

    success = vector_store(documents , source = file.filename)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to store vectors.")

    return {"message": "File uploaded successfully.", "chunks": len(documents)}


@app.get("/query")
async def query(q: str):
    try:

        hyde_answer = hyde(q)
        search_results = hybrid_search(hyde_answer)
        print("search_results")
        print(search_results)
        print("=" * 30)
        reranked_docs = rerank(search_results , q)
        print("reranked_docs")
        print(reranked_docs)
        print("=" * 30)
        compressed = compress(reranked_docs , q)
        print("compressed")
        print(compressed)
        print("=" * 30)
        final_answer = generate(q , compressed)

        answers = final_answer.split("\n\n")
        return {"answer" : answers}
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

