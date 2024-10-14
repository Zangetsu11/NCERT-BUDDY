import faiss
import numpy as np
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from sklearn.metrics.pairwise import cosine_similarity

# Load embeddings and FAISS index
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
index = faiss.IndexFlatL2(384)  # Ensure this matches your embedding dimension
vector_store = FAISS(embedding_function=embeddings, index=index, docstore=InMemoryDocstore(), index_to_docstore_id={})

# Predefined sound-related queries to establish a baseline
baseline_queries = complete_sound_questions = [
    # General Questions About Sound
    "What is sound ?",
    "What is wavelength",
    "Explain the properties of sound waves.",
    "How does sound travel through different media?",
    "What is frequency, and how does it relate to pitch?",
    "Describe the relationship between pitch and amplitude.",
    "What are the effects of sound on the human body?",
    
    # Production of Sound
    "How do different materials affect sound production?",
    "How do musical instruments produce sound?",
    
    # Propagation of Sound
    "Explain the difference between longitudinal and transverse waves.",
    "What are the characteristics of sound waves?",
    "How does temperature affect the speed of sound in various media?",
    
    # Reflection of Sound
    "What is the principle behind the reflection of sound?",
    "Describe the phenomenon of echo and its applications.",
    "What is reverberation, and how does it differ from echo?",
    "What are practical applications of multiple reflections of sound?",
    
    # Range of Hearing
    "What is the range of human hearing, and how does it change with age?",
    
    # Applications of Ultrasound
    "What are the uses of ultrasound in medical and industrial fields?",
    "How is ultrasound utilized in diagnostics and treatment?",
    "What are the advantages of using ultrasound over other imaging techniques?",
    
    # Additional Concepts
    "What is the difference between loudness and intensity of sound?",
    "Explain sound wave interference and its effects.",
    "How do acoustic devices (like microphones and speakers) work?",
    "What is Doppler effect, and how does it relate to sound?"
]


# Embed the baseline queries
baseline_embeddings = np.array([embeddings.embed_query(query) for query in baseline_queries])
SIMILARITY_THRESHOLD = 0.5  # Adjust as needed

def is_confident_query(query):
    query_embedding = embeddings.embed_query(query)
    similarities = cosine_similarity([query_embedding], baseline_embeddings)
    max_similarity = similarities.max()
    print(f"Max Similarity: {max_similarity:.4f}")  # Print the similarity value
    if max_similarity < SIMILARITY_THRESHOLD:
        return False, "Please ask a more specific question about sound!"
    return True, ""


def embed_chunks(chunks):
    for chunk in chunks:
        embedding = embeddings.embed_query(chunk.page_content)
        index.add(np.array([embedding]))

def get_embeddings_and_index(chunks):
    embed_chunks(chunks)
    return index
