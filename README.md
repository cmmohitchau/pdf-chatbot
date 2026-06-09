# 😎 Retrieval Augmented Generation (RAG) 

A curated resource map of tools, frameworks, techniques, and learning materials for building Retrieval-Augmented Generation (RAG) systems. This repository catalogs the RAG ecosystem and provides links to authoritative sources, tutorials, and implementations to help you explore and build RAG applications.

## Overview

**Retrieval-Augmented Generation (RAG)** is a sophisticated technique in Generative AI that enhances Large Language Models (LLMs) by dynamically retrieving and incorporating relevant context from external knowledge sources during the generation process. Unlike traditional LLMs that rely solely on pre-trained knowledge, RAG systems enable models to access up-to-date, domain-specific, or proprietary information, significantly improving accuracy, reducing hallucinations, and enabling real-time knowledge integration.

### Key Benefits

- **Reduced Hallucinations**: Grounds responses in retrieved factual information
- **Domain Adaptation**: Enables LLMs to work with specialized knowledge without fine-tuning
- **Real-time Updates**: Incorporates latest information without model retraining
- **Cost Efficiency**: More economical than fine-tuning for domain-specific tasks
- **Transparency**: Provides source attribution for generated content
- **Privacy & Security**: Keeps sensitive data in private knowledge bases

## ℹ️ General Information on RAG

RAG addresses a fundamental limitation of LLMs: their static knowledge cutoff and inability to access external information. Traditional RAG implementations employ a retrieval pipeline that enriches LLM prompts with contextually relevant documents from a knowledge base. For example, when querying about renovation materials for a specific house, the LLM may have general renovation knowledge but lacks details about that particular property. An RAG system can retrieve relevant documents (e.g., blueprints, material specifications, local building codes) to provide accurate, context-aware responses.

## 🏗️ Architecture
<img width="2069" height="1227" alt="rag-architecture" src="https://github.com/user-attachments/assets/7d9fb1df-7937-41f9-b03b-7010b658ffac" />

## 🛠️ Techniques

### Chunking
  - **[Recursive Chunking](https://medium.com/@AbhiramiVS/chunking-methods-all-to-know-about-it-65c10aa7b24e)**
  - **Use Case**: Documents with hierarchical structure (markdown, HTML, code)
  - **Characteristics**: Recursively splits by separators (paragraphs → sentences → words) until desired chunk size
  - **Pros**: Preserves natural boundaries, respects document hierarchy, better semantic coherence
  - **Cons**: More complex, variable chunk sizes, requires careful separator configuration
  - **Implementation**: [RecursiveCharacterTextSplitter](https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/recursive_text_splitter/)       (LangChain)

### Embeddings
  Embeddings are the foundation of semantic search in RAG systems. The choice of embedding model significantly impacts retrieval quality.

  Embedding is done with **text-embedding-3-small** model

### Retrieval

- **HyDE** : Query is invoked to LLM to generate Hypothetical scientific answer for better vector search.
- **Hybrid Search** : (vector search + BM25) vector search is used for semantic search whereas BM25 is used for keyword search.
- **Rerank and Compression** : Rerank is used to rank top 10 documents and compression is used to remove the unnecessary noise in the document.

### Generation

  The compressed docs and query is passed to LLM to generate the final answer.


  
