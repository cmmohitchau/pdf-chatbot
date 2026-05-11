from pypdf import PdfReader

def load_documents(file):
    print("Loading documents...")
    try:
        reader = PdfReader(file.file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted
            
        return text
    except Exception as e:
        print(f"Error loading document: {e}")
        return None

