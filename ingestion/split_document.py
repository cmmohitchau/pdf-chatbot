from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
def split_document(pages , source):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        for page in pages:
            print(page)
            print("=" * 30 + "\n\n")
        

        document = []

        for page_num, page in enumerate(pages):
            chunks = text_splitter.split_text(page)
           
            for chunk_id , chunk in enumerate(chunks):
                document.append(
                    Document(
                        page_content=chunk,
                        metadata={"source" : source , "page" : page_num + 1 , "chunk_id" : chunk_id + 1}
                    )
                )
        return document
    except Exception as e:
        print(f"Error parsing document: {e}")
        return None