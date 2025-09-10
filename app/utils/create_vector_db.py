from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Paths
DATA_PATH = "app/data/course_data.json"
VECTOR_DB_DIR = "app/data/chroma_db"

# Load JSON data as documents
loader = JSONLoader(
    file_path=DATA_PATH,
    jq_schema=".",      # Load all top-level JSON entries
    text_content=False  # Preserve metadata
)
data = loader.load()

# Split large text into smaller chunks for embeddings
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0
)
all_splits = text_splitter.split_documents(data)

# Initialize Ollama embeddings (local model)
local_embeddings = OllamaEmbeddings(model="nomic-embed-text")  # adjust to your local Ollama model

# Create Chroma vector store from chunks
vectorstore = Chroma.from_documents(documents=all_splits, embedding=local_embeddings, persist_directory=VECTOR_DB_DIR)
# Persist the vector store to disk

print(f"Vector database created and saved at: {VECTOR_DB_DIR}")
