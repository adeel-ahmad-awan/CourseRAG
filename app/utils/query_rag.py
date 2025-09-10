import json
import numpy as np
from langchain_ollama import OllamaEmbeddings, ChatOllama

VECTOR_DB_PATH = "app/data/course_vectors.faiss"
METADATA_PATH = "app/data/course_metadata.json"

# Initialize Ollama client
ollama = ChatOllama(model="llama2-7b")  # Or your preferred model

# Load FAISS index
index = faiss.read_index(VECTOR_DB_PATH)

# Load metadata
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)


def embed_query(query):
    """Generate embedding for a query using Ollama."""
    try:
        embedding = OllamaEmbeddings(model="llama2-7b").embed_query(query)
        return np.array(embedding).astype("float32")
    except Exception as e:
        print(f"[Error] Failed to embed query: {e}")
        return None


def query_rag(query, top_k=3):
    """Retrieve top-k matching courses from FAISS index."""
    query_vec = embed_query(query)
    if query_vec is None:
        return []

    query_vec = np.expand_dims(query_vec, axis=0)
    distances, indices = index.search(query_vec, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])
    return results


def answer_query(query, top_k=3, show_context=False):
    """Retrieve relevant courses and generate an answer using Ollama."""
    matches = query_rag(query, top_k=top_k)

    if not matches:
        return "No relevant courses found."

    # Combine text for model input
    context_texts = [f"{match['title']} - {match['url']}" for match in matches]
    context = "\n".join(context_texts)

    # Generate answer
    try:
        response = ollama.generate(
            messages=[
                {"role": "system", "content": "You are a helpful assistant answering questions about training courses."},
                {"role": "user", "content": f"Answer this question based on the following courses:\n{context}\n\nQuestion: {query}"}
            ]
        )
        return response.generations[0].text
    except Exception as e:
        return f"Error generating response: {e}"


