from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

chunk_id = 0

def split_document(pages , source):
    global chunk_id
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
        document = []

        for page_num, page in enumerate(pages):
            chunks = text_splitter.split_text(page)
           
            for chunk_index_in_page , chunk in enumerate(chunks):
                chunk_id += 1
                document.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "source" : source,
                            "page" : page_num + 1 ,
                            "chunk_id" : chunk_id,
                            "chunk_index_in_page" : chunk_index_in_page + 1
                            }
                    )
                )
        return document
    except Exception as e:
        print(f"Error parsing document: {e}")
        return None