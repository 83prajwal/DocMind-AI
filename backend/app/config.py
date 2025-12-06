from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    chroma_persist_directory: str = "../data/chromadb"
    upload_directory: str = "../data/uploads"
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    class Config:
        env_file = ".env"

settings = Settings()