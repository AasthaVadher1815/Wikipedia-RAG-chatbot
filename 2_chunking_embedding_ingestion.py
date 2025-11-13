#################################################################################################################################################################
###############################   1.  IMPORTING MODULES AND INITIALIZING VARIABLES   ############################################################################
#################################################################################################################################################################

from dotenv import load_dotenv
import os
import shutil
from uuid import uuid4

# ✅ Updated imports for modern LangChain setup
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

#################################################################################################################################################################
###############################   2.  LOAD ENVIRONMENT VARIABLES AND INITIALIZE EMBEDDINGS MODEL   ###############################################################
#################################################################################################################################################################

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
DATABASE_LOCATION = os.getenv("DATABASE_LOCATION")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
DATASET_STORAGE_FOLDER = os.getenv("DATASET_STORAGE_FOLDER")

# 🔍 Validate environment
if not all([EMBEDDING_MODEL, DATABASE_LOCATION, COLLECTION_NAME, DATASET_STORAGE_FOLDER]):
    raise EnvironmentError("❌ Missing one or more required environment variables in .env file")

# ✅ Initialize embeddings model
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

#################################################################################################################################################################
###############################   3.  DELETE EXISTING CHROMA DATABASE IF EXISTS   ################################################################################
#################################################################################################################################################################

if os.path.exists(DATABASE_LOCATION):
    shutil.rmtree(DATABASE_LOCATION)
    print(f"🗑️ Old database removed at {DATABASE_LOCATION}")

# ✅ Initialize vector store
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=DATABASE_LOCATION,
)

#################################################################################################################################################################
###############################   4.  INITIALIZE TEXT SPLITTER   #################################################################################################
#################################################################################################################################################################

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

#################################################################################################################################################################
###############################   5.  LOAD AND PROCESS PLAIN TEXT DATA   ########################################################################################
#################################################################################################################################################################

data_path = os.path.join(DATASET_STORAGE_FOLDER, "data.txt")

if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Could not find data file at: {data_path}")

print(f"📖 Loading data from: {data_path}")

with open(data_path, "r", encoding="utf-8") as f:
    text_data = f.read().strip()

if not text_data:
    raise ValueError("❌ data.txt is empty. Please run 1_scraping_wikipedia.py first.")

#################################################################################################################################################################
###############################   6.  CHUNKING, EMBEDDING AND INGESTION   #######################################################################################
#################################################################################################################################################################

print("✂️ Splitting text into chunks...")
chunks = text_splitter.create_documents([text_data])

print(f"🧩 Created {len(chunks)} text chunks. Now generating embeddings...")

# Generate UUIDs for each chunk
uuids = [str(uuid4()) for _ in range(len(chunks))]

# Add chunks to the vector store
vector_store.add_documents(documents=chunks, ids=uuids)

# ✅ No need to call persist() — Chroma auto-saves now
print("✅ All chunks embedded and automatically saved to Chroma vector store.")
print(f"📁 Database location: {DATABASE_LOCATION}")
print(f"📚 Collection name: {COLLECTION_NAME}")
print(f"🔢 Total chunks ingested: {len(chunks)}")
