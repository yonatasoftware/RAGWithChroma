import os,json,chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false" # To suppress parallelism warnings from the tokenizers library, which can occur when using multiple threads for tokenization. This setting ensures that the library operates in a single-threaded mode, preventing potential issues related to concurrent access and improving stability during execution.
# LLM 
Groq_client=Groq(api_key=os.getenv('GROQ_API_KEY'))

# -----------------------------
# Load embedding model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Connect to ChromaDB
# -----------------------------
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_collection(
    name="insurance_policy"
)

# -----------------------------
# User Query
# -----------------------------
age=input('Age: ')
exp=input('Driving Experience (years): ')
acc=input('Previous Accidents: ')
val=input('Vehicle Value (₹): ')
# User Prompt
user_prompt=f'Age: {age}\nDriving Experience: {exp} years\nPrevious Accidents: {acc}\nVehicle Value: ₹{val}'

# -----------------------------
# Create query embedding
# -----------------------------
query_embedding = model.encode(user_prompt).tolist()

# -----------------------------
# Search ChromaDB
# -----------------------------
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

# =====================================================
# Print Raw Chroma Response
# =====================================================

print("\nRaw ChromaDB Response")
print("=" * 100)

print(json.dumps(results, indent=4))

# =====================================================
# Print Retrieved Chunks
# =====================================================

print("\nRetrieved Chunks")
print("=" * 100)

documents = results["documents"][0]
ids = results["ids"][0]
distances = results["distances"][0]
metadatas = results["metadatas"][0]

for rank in range(len(ids)):

    print(f"\nRank         : {rank + 1}")
    print(f"Chunk ID     : {ids[rank]}")
    print(f"Distance     : {distances[rank]:.4f}")
    print(f"Start Index  : {metadatas[rank]['start_index']}")
    print(f"End Index    : {metadatas[rank]['end_index']}")

    print("-" * 80)

    print(documents[rank])

    print("=" * 100)

# =====================================================
# Build Context for LLM
# =====================================================

context = "\n\n".join(documents)

print("\nContext Sent To LLM")
print("=" * 100)

print(context)

print("=" * 100)

system=f'''You are an automobile insurance underwriter.
Use ONLY the following policy:
{context}
Return ONLY a valid JSON object.

Do NOT use markdown.
Do NOT wrap the response in triple backticks.
Do NOT include explanations.
{
    {
        "risk_level":"",
        "premium_band":"",
        "decision":"",
        "matched_rules":[]
    }
}'''
response=Groq_client.chat.completions.create(
    model='openai/gpt-oss-20b',
    temperature=0,
    messages=[
        {'role':'system',
         'content':system},
        {'role':'user',
         'content':user_prompt}
        ])
print(response.choices[0].message.content)