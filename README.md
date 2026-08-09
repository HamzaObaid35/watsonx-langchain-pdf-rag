# 📄 PDF RAG Question Answering Bot

A Retrieval-Augmented Generation (RAG) application that allows users to upload a PDF document and ask questions about its content.

This project was developed as part of the **Generative AI Engineering with LLMs** learning track and demonstrates a complete document-question-answering pipeline using LangChain, IBM watsonx.ai, ChromaDB, and Gradio.

## 🚀 Features

- Upload a PDF document
- Extract text with `PyPDFLoader`
- Split documents into overlapping chunks
- Generate embeddings with IBM watsonx.ai
- Store embeddings in ChromaDB
- Retrieve relevant document chunks with similarity search
- Generate answers with an IBM Granite LLM
- Interact through a Gradio web interface

## 🧠 Architecture

```text
PDF Document
     ↓
PyPDFLoader
     ↓
RecursiveCharacterTextSplitter
     ↓
IBM watsonx.ai Embeddings
     ↓
Chroma Vector Database
     ↓
Retriever
     ↓
RetrievalQA
     ↓
IBM Granite LLM
     ↓
Gradio Interface
```

## 🛠️ Technologies

- Python
- LangChain
- IBM watsonx.ai
- IBM Granite
- ChromaDB
- Gradio
- PyPDF

## 🤖 Models

**LLM**

```text
ibm/granite-4-h-small
```

**Embedding model**

```text
ibm/granite-embedding-278m-multilingual
```

> Note: The course lab originally referenced an older Slate embedding model. This repository uses the currently supported Granite embedding model for compatibility with the active watsonx.ai endpoint.

## 📂 Project Structure

```text
pdf-rag-qa-bot/
│
├── qabot.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    └── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/pdf-rag-qa-bot.git
cd pdf-rag-qa-bot
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

```bash
python qabot.py
```

The application is configured to run on port `7860`.

## 📖 How It Works

1. The user uploads a readable PDF document.
2. `PyPDFLoader` extracts the document text.
3. `RecursiveCharacterTextSplitter` divides the text into chunks of 1000 characters with an overlap of 200.
4. IBM watsonx.ai generates vector embeddings for the chunks.
5. ChromaDB stores the embeddings.
6. A vector-store retriever finds the document chunks most relevant to the user's question.
7. `RetrievalQA` sends the retrieved context and question to the Granite LLM.
8. The answer is displayed in the Gradio interface.

## 📸 Demo

Place a screenshot of the working application in:

```text
screenshots/qa_bot.png
```

Then replace this note with:

```markdown
![PDF Q&A Bot](screenshots/qa_bot.png)
```

## 🎓 Project Context

This repository is an educational implementation created while completing the final RAG project in the Generative AI Engineering with LLMs learning track.

The project demonstrates the integration of:

- document loading
- text splitting
- embeddings
- vector databases
- retrieval
- LLM-based question answering
- a Gradio user interface

## 🔧 Compatibility Update

While completing the lab, the original embedding model referenced by the course was no longer supported by the active IBM watsonx.ai endpoint.

The implementation therefore uses:

```text
ibm/granite-embedding-278m-multilingual
```

This keeps the project functional while preserving the intended RAG architecture of the lab.

## ⚠️ Notes

- Best suited for readable PDF documents.
- Very large PDFs may require batching, persistent vector storage, or additional optimization.
- Do not commit API keys, credentials, `.env` files, or virtual environments to GitHub.
- The `skills-network` project configuration is intended for the IBM Skills Network lab environment. Running the project outside that environment may require your own IBM Cloud credentials and project configuration.

## 📄 License

This project is intended for educational and portfolio use.
