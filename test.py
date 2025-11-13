from dotenv import load_dotenv
import os

load_dotenv()

print("Embedding model:", os.getenv("EMBEDDING_MODEL"))
print("Chat model:", os.getenv("CHAT_MODEL"))
print("Dataset folder:", os.getenv("DATASET_STORAGE_FOLDER"))
print("Chroma DB:", os.getenv("DATABASE_LOCATION"))
