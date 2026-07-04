
import chromadb
from sentence_transformers import SentenceTransformer

# Import utility functions
from utility import extract_pdf_text, chunk_text

import os

print("Current Working Directory:")
print(os.getcwd())

# Step 1 Extract PDF Text
PDF = "policy.pdf"
policyData = extract_pdf_text(PDF)

# Step 2 Chunk Text 
chunks = chunk_text(
    policyData,
    chunk_size=500,
    chunk_overlap=100
)

print(f"\nTotal Chunks Created : {len(chunks)}\n")

# Step 3 : Create Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
chunk_texts = [chunk["text"] for chunk in chunks]

embeddings = model.encode(chunk_texts).tolist()

# Create persistent Chroma database
client = chromadb.PersistentClient(path="./chroma_db")

collection_name = "insurance_policy"

# Delete existing collection if it exists
try:
    client.delete_collection(collection_name)
except Exception:
    pass

collection = client.create_collection(collection_name)

# Add each chunk
for chunk, embedding in zip(chunks, embeddings):

    collection.add(
    ids=[str(chunk["chunk_id"])],
    embeddings=[embedding],
    documents=[chunk["text"]],
    metadatas=[
        {
            "chunk_id": chunk["chunk_id"],
            "start_index": chunk["start_index"],
            "end_index": chunk["end_index"]
        }
    ]
)

print("Documents successfully added to ChromaDB.")


print(f"Total Chunks Created : {len(chunks)}")
print(f"Embedding Dimension  : {len(embeddings[0])}")
    
