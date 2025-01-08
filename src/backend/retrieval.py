import chromadb
from chromadb.config import Settings
import time
from langchain.embeddings.openai import OpenAIEmbeddings

client = chromadb.PersistentClient(path="./chroma_db_storage")
collection = client.get_or_create_collection("chat_history")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
def retrieve_documents_from_db(query: str, n: int):
    ### Retrieve from vector db###    
 
    query_embedding = get_openai_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n
    )
    return results

def add_document_to_db(thread_id: str, document: str):        
        collection.add(
        ids=thread_id + "_" + str(int(time.time() * 1000)),
        documents=[document],            
        embeddings=[get_openai_embedding(document)]
    )


def get_openai_embedding(text: str):
    document_embedding = embeddings.embed_query(text)
    return document_embedding
# retrieve_documents_from_db("How do I search for people given their current title, current company and location? Also can you verify it")