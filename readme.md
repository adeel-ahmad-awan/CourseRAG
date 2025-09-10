# **Flask RAG Application**

This project is a **Retrieval-Augmented Generation (RAG)** application built with **Flask**, **LangChain**, and **Ollama**. It extracts course data from web pages, indexes it into a vector database, and allows users to query relevant training courses with natural language questions.

The pipeline works as follows:

1. **Data Extraction** → Scrapes course data (title, description, outcomes, etc.) into structured JSON.  
2. **Vector Database Creation** → Splits and embeds the extracted text using **Ollama embeddings**, stored in a **Chroma / FAISS** vector database.  
3. **Query & Retrieval** → User queries are embedded and matched against the vector DB for the most relevant results.  
4. **Answer Generation** → A local Ollama LLM (e.g., llama2-7b) generates a contextual response with course recommendations.

## **Getting Started**

### **1\. Install Dependencies**

Make sure you have Python 3.9+ installed.

It’s recommended to use a virtual environment to keep dependencies isolated:



```
# Create virtual environment (Linux/Mac)
python3 -m venv venv

# Or on Windows
python -m venv venv

# Activate the environment
# Linux/Mac
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\activate
```
Then install required packages:
```
pip install \-r requirements.txt
```

### **2\. Install & Run Ollama**

This app relies on [**Ollama**](https://ollama.ai/) for local LLMs and embeddings.

Download Ollama and pull required models:

```
ollama pull llama2:7b  
ollama pull nomic-embed-text
```

### **3\. Extract Course Data**

Scrape course pages and save them into app/data/course\_data.json:

```
python app/data\_extractor.py
```

### **4\. Build Vector Database**

Create embeddings and store them in **Chroma**:

```
python app/create\_vector\_db.py
```

### **5\. Run Query Tests**

(If you’ve added a Flask API/Frontend layer, run it here)

flask run \--reload  
---

## **🔑 Key Components**

### **data\_extractor.py**

* Scrapes course websites using requests \+ BeautifulSoup.

* Extracts fields like title, description, topics, learning outcomes, prerequisites, and schedules.

* Saves results in structured JSON.

### **create\_vector\_db.py**

* Loads JSON course data.

* Splits text into chunks for embeddings.

* Uses **Ollama embeddings (nomic-embed-text)**.

* Saves vector store (Chroma by default).

### **query\_rag.py**

* Embeds user queries with Ollama.

* Retrieves top-k matches from FAISS/Chroma.

* Generates a contextual answer using **LLaMA-2 (7B)**.

---

## **🛠️ Customization**

* Change Ollama models (llama2-7b, mistral, nomic-embed-text, etc.) in scripts.

* Adjust top\_k for retrieval depth.

* Modify jq\_schema in create\_vector\_db.py if your JSON structure changes.

* Extend Flask endpoints to support **chat history, multi-turn conversations, or fine-grained search filters**.

---

## **📌 Roadmap / Next Steps**

* Add Flask routes for query/answer endpoints

* Create a simple frontend (React or HTML templates)

* Support multiple data sources (PDFs, CSVs, APIs)

* Implement hybrid search (BM25 \+ embeddings)

* Add course filtering (by date, level, provider)