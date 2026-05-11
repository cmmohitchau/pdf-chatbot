from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
def split_document(text , source):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text)

        document = []
        for chunk in chunks:

            document.append(
                Document(
                    page_content=chunk,
                    metadata={"source": source}
                )
            )        
        return document
    except Exception as e:
        print(f"Error parsing document: {e}")
        return None