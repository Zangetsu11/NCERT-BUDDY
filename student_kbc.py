from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import random
from document_loader import load_documents

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def generate_question(context):
    prompt = (
        "You are a helpful assistant designed to generate quiz questions. Based on the provided content, create a quiz question that includes both a numerical component and an objective question. Provide four answer options labeled A, B, C, D, and indicate the correct answer at the end. Ensure that the question tests comprehension and is under 200 characters to avoid token limit issues."
    )

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"{context}"}
    ]

    client = InferenceClient(api_key=HUGGINGFACE_API_KEY)
    response = ""

    for message in client.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=messages,
        max_tokens=250,
        stream=True,
    ):
        response += message.choices[0].delta.content

    # print("Raw Response from API:", response.strip())

    return response.strip()

if __name__ == "__main__":
    file_path = "data/ncert.pdf" 
    chunks = load_documents(file_path)

    context = random.choice(chunks).page_content
    
    # Generate question based on the random chunk
    question = generate_question(context)
    print("Generated Question:", question)