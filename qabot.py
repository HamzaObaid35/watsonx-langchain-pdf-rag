# ============================================================
# PDF Q&A Bot using LangChain, IBM watsonx.ai, Chroma & Gradio
# Final Project
# ============================================================

from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from ibm_watsonx_ai import Credentials

from langchain_ibm import WatsonxLLM, WatsonxEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA

from huggingface_hub import HfFolder

import gradio as gr
import warnings


# ============================================================
# Suppress warnings
# ============================================================

def warn(*args, **kwargs):
    pass


warnings.warn = warn
warnings.filterwarnings("ignore")


# ============================================================
# LLM
# ============================================================

def get_llm():
    model_id = "ibm/granite-4-h-small"

    parameters = {
        GenParams.MAX_NEW_TOKENS: 256,
        GenParams.TEMPERATURE: 0.5,
    }

    project_id = "skills-network"

    watsonx_llm = WatsonxLLM(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id=project_id,
        params=parameters,
    )

    return watsonx_llm


# ============================================================
# Task 1: Document Loader
# ============================================================

def document_loader(file):
    if hasattr(file, "name"):
        file_path = file.name
    else:
        file_path = file

    loader = PyPDFLoader(file_path)
    loaded_document = loader.load()

    return loaded_document


# ============================================================
# Task 2: Text Splitter
# ============================================================

def text_splitter(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = splitter.split_documents(data)

    return chunks


# ============================================================
# Task 3: Embedding Model
# ============================================================

def watsonx_embedding():
    # The original lab referenced ibm/slate-125m-en.
    # The current Skills Network watsonx endpoint supports
    # ibm/granite-embedding-278m-multilingual instead.
    return WatsonxEmbeddings(
        model_id="ibm/granite-embedding-278m-multilingual",
        url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
    )


# ============================================================
# Task 4: Vector Database
# ============================================================

def vector_database(chunks):
    embedding_model = watsonx_embedding()

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
    )

    return vectordb


# ============================================================
# Task 5: Retriever
# ============================================================

def retriever(file):
    splits = document_loader(file)
    chunks = text_splitter(splits)
    vectordb = vector_database(chunks)

    return vectordb.as_retriever()


# ============================================================
# Task 6: QA Chain
# ============================================================

def retriever_qa(file, query):
    llm = get_llm()
    retriever_obj = retriever(file)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever_obj,
        return_source_documents=True,
    )

    response = qa.invoke(query)

    return response["result"]


# ============================================================
# Gradio Interface
# ============================================================

rag_application = gr.Interface(
    fn=retriever_qa,
    inputs=[
        gr.File(
            label="Upload PDF File",
            file_count="single",
            file_types=[".pdf"],
            type="filepath",
        ),
        gr.Textbox(
            label="Input Query",
            lines=2,
            placeholder="Type your question here...",
        ),
    ],
    outputs=gr.Textbox(label="Output"),
    title="PDF Q&A Bot",
    description=(
        "Upload a PDF document and ask any question. "
        "The chatbot will try to answer using the provided document."
    ),
    allow_flagging="never",
)


# ============================================================
# Launch Application
# ============================================================

if __name__ == "__main__":
    rag_application.launch(
        server_name="0.0.0.0",
        server_port=7860,
    )
