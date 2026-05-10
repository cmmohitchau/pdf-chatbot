from PyPDF2 import PdfReader

def load_documents(file_path):
    print("Loading documents...")
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        print("Document loaded successfully.")
        return text
    except Exception as e:
        print(f"Error loading document: {e}")
        return None

