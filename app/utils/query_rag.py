# app/utils/query_rag.py
from langchain_chroma import Chroma
from .embeddings_functions import get_embedding_function
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

VECTOR_DB_DIR = "app/data/chroma_db"
embedding_fn = get_embedding_function()
MODEL = Ollama(model="mistral")

PROMPT_TEMPLATE = """
You are an assistant for question-answering tasks. Use the following retrieved context to answer the question.
If you don't know the answer, say so. Keep it concise.

<context>
{context}
</context>

Question: {question}
"""



def is_valid_question(user_input: str) -> bool:
    model = Ollama(model="mistral")
    prompt = f"""
    Decide if this input is a real question in English about courses. 
    If it looks like random letters or nonsense, say "INVALID". 
    Otherwise, say "VALID". 
    Answer only with VALID or INVALID.

    Input: "{user_input}"
    """
    response = model.invoke(prompt).strip().upper()
    print("response isValid_question:", response)
    return response.startswith("VALID")

def query_rag(query_text: str):

    if not is_valid_question(query_text):
        response_text = "I couldn’t understand your question. Please ask about courses."
        sources = "No valid sources found."
        return response_text, sources

    # Reload DB
    db = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embedding_fn)

    # Retrieve top 5 results
    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    # Format prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Generate response
    response_text = MODEL.invoke(prompt)

    # Include source info (titles or URLs)
    sources = [doc.metadata.get("title", doc.metadata.get("url", None)) for doc, _ in results]
    return response_text, sources