import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings

class ChromaDBService:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False,  # Already here
                allow_reset=True
            )
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, texts: list, metadatas: list, ids: list):
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def query_documents(self, query: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    
    def reset(self):
        self.client.delete_collection("documents")
        self.collection = self.client.get_or_create_collection(name="documents")

chroma_service = ChromaDBService()