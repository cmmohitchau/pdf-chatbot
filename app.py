from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import select
from ingestion.load_documents import load_documents
from ingestion.split_document import split_document
from ingestion.vector_store import vector_store
from retrieval.hyde import hyde
from retrieval.hybrid_search import hybrid_search
from retrieval.rerank_compression import (rerank , compress)
from generation.generate import generate
from db.engine import create_db_and_tables
from db.model import User , UserCreate
from db.engine import SessionDep
from contextlib import asynccontextmanager
from db.crud import create_user, get_user_by_email, jwt_authenticate, sign_user
from middleware import AuthMiddleware
from auth.google import router
from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    sources: Optional[List[str]] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

origins = [
   "https://pdf-chat-frontend-cyan.vercel.app",
   "http://localhost:3000"
]

app.add_middleware(
CORSMiddleware,
allow_origins=origins, 
allow_credentials=True, 
allow_methods=["*"], 
allow_headers=["*"], 
)
app.add_middleware(AuthMiddleware)

ALLOWED_CONTENT_TYPES = {"application/pdf"}

@app.get("/")
async def root():
    return {"message": "RAG API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/signup")
def signup(user: UserCreate, session : SessionDep):
    return create_user(user=user, session=session)

@app.post("/signin")
def signin(user: UserCreate, session:SessionDep):
    return sign_user(user=user , session=session)

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


@app.post("/query")
async def query(queryRequest: QueryRequest , request: Request):
    try:
        q = queryRequest.query
        sources = queryRequest.sources

        if(not sources):
            return {"answer" : "Please specify the source document for accurate information." , "citations" : []}
        

        hyde_answer = hyde(q)
        search_results = hybrid_search(hyde_answer, sources=sources)
        reranked_docs = rerank(search_results , q)

        compressed = compress(reranked_docs)

        final_answer = generate(q , compressed["context"])

        return {
            "answer" : final_answer.content,
            "citations" : compressed["citations"]
        }
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

