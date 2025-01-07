from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(path="./chroma_db_storage")
collection = client.get_or_create_collection("chat_history")
def retrieve_documents_from_db(query):
    ### Retrieve from vector db###    
 
    model = SentenceTransformer('all-MiniLM-L6-v2')

    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    if results["documents"]:
        return results["documents"]
    return [[]]

# retrieve_documents_from_db("How do I search for people given their current title, current company and location? Also can you verify it")