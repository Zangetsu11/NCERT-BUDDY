from query_handler import handle_query
from document_loader import load_documents
from embeddings import get_embeddings_and_index

chunks = []

def startup():
    global chunks
    file_path = "data/ncert.pdf"
    chunks = load_documents(file_path)
    get_embeddings_and_index(chunks)

def query_console():
    while True:
        user_query = input("Enter your question about sound (enter 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        else:
            try:
                response = handle_query(user_query, chunks)
                print("Response:", response["response"])
            except Exception as e:
                print("Error:", str(e))

if __name__ == "__main__":
    startup()
    query_console()