from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from embeddings_functions import get_embedding_function
from langchain.schema import Document
import json

DATA_PATH = "app/data/course_data.json"
VECTOR_DB_DIR = "app/data/chroma_db"

def load_courses(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for _, course in data.items():
        # Build text content
        title = course.get("title", "")
        description = " ".join(course.get("description", []))
        topics = ", ".join(course.get("topics_covered", []))
        outcomes = ", ".join(course.get("learning_outcomes", []))
        prerequisites = ", ".join(course.get("prerequisites", []))

        page_content = f"""
        Title: {title}
        Description: {description}
        Topics Covered: {topics}
        Learning Outcomes: {outcomes}
        Prerequisites: {prerequisites}
        """

        # Metadata
        metadata = {
            "url": course.get("url", ""),
            "level": ", ".join(course.get("level", [])),
            "upcoming_courses": ", ".join([c.get("title", "") for c in course.get("upcoming_courses", [])]),
            "previous_courses": ", ".join([c.get("title", "") for c in course.get("previous_courses", [])])
        }

        docs.append(Document(page_content=page_content.strip(), metadata=metadata))

    return docs

# Load data
data = load_courses(DATA_PATH)


# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_splits = text_splitter.split_documents(data)

# Embeddings
embedding_fn = get_embedding_function()

# Vector store
vectorstore = Chroma.from_documents(
    documents=all_splits,
    embedding=embedding_fn,
    persist_directory=VECTOR_DB_DIR
)

print(f"Vector database created and saved at: {VECTOR_DB_DIR}")
