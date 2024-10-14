from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(file_path):
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    
    # print(f"Loaded {len(docs)} documents from {file_path}")
    
    def clean_metadata(metadata):
        keys_to_keep = ['title', 'author', 'creationDate', 'modDate', 'total_pages']
        return {key: metadata[key] for key in keys_to_keep if key in metadata}
    
    cleaned_metadata = clean_metadata(docs[0].metadata)
    # print("Document metadata:", cleaned_metadata)

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=25)
    chunks = text_splitter.split_documents(docs)
    
    # print(chunks[0])

    return chunks
