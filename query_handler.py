import numpy as np
from embeddings import embeddings, index, is_confident_query
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def handle_query(user_query: str, chunks):
    is_confident, message = is_confident_query(user_query)
    if is_confident:
        query_embedding = embeddings.embed_query(user_query)
        k_nearest = 5
        D, I = index.search(np.array([query_embedding]), k_nearest)

        context_chunks = [(distance, chunks[index].page_content) for distance, index in zip(D[0], I[0])]
        context = "\n".join(chunk for _, chunk in context_chunks)

        prompt = (
            "You are a helpful assistant designed to help students understand concepts from a PDF. If a user asks a question related to the content, provide clear, concise notes that simplify the information for easy understanding. Focus on key points and explanations that enhance comprehension.Ensure that the notes generated are complete, concise and under 300 characters to avoid token limit issues."
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{context}\n\n{user_query}"}
        ]

        client = InferenceClient(api_key=HUGGINGFACE_API_KEY)
        response = ""

        for message in client.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=messages,
            max_tokens=500,
            stream=True,
        ):
            response += message.choices[0].delta.content
        
        return {"response": response}
    else:
        return {"response": "Hello, I would be happy to help you with queries regarding the chapter 'SOUND'."}
