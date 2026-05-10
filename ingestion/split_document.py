from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_document(text):
    print("Parsing document...")
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text)
        print(f"Document parsed into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        print(f"Error parsing document: {e}")
        return None