#########################################################################################################
###############################   1. IMPORTS AND ENV SETUP   ############################################
#########################################################################################################

import streamlit as st
from dotenv import load_dotenv
import os

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

#########################################################################################################
###############################   2. LOAD ENVIRONMENT VARIABLES   #######################################
#########################################################################################################

load_dotenv()

DATABASE_LOCATION = os.getenv("DATABASE_LOCATION", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "local_rag_collection")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:1b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")

#########################################################################################################
###############################   3. INITIALIZE EMBEDDINGS AND VECTOR DB   ##############################
#########################################################################################################

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=DATABASE_LOCATION,
)

#########################################################################################################
###############################   4. INITIALIZE CHAT MODEL   ############################################
#########################################################################################################

llm = ChatOllama(model=LLM_MODEL, temperature=0.2)

#########################################################################################################
###############################   5. STREAMLIT UI SETUP   ###############################################
#########################################################################################################

st.set_page_config(page_title="Local RAG Chatbot 💬", layout="centered")
st.title("💬 Local RAG Chatbot with Ollama")
st.caption("Ask questions based on your locally embedded Wikipedia data.")

#########################################################################################################
###############################   6. CHAT INTERFACE   ###################################################
#########################################################################################################

query = st.text_input("🔍 Enter your question:")

if query:
    st.write(f"**You asked:** {query}")

    # Embed query
    query_vector = embeddings.embed_query(query)

    # Retrieve similar documents
    results = vector_store.similarity_search_by_vector(query_vector, k=3)

    context = "\n\n".join([doc.page_content for doc in results])

    st.write("📚 **Relevant context:**")
    st.info(context[:1000] + "..." if len(context) > 1000 else context)

    # Generate answer using Ollama
    prompt = f"Answer the following question using the provided context.\n\nContext:\n{context}\n\nQuestion: {query}"
    response = llm.invoke(prompt)

    st.write("🤖 **Answer:**")
    st.success(response.content)

#########################################################################################################
###############################   END OF FILE   #########################################################
#########################################################################################################
