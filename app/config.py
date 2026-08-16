from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    groq_api_key:str
    groq_model: str = "openai/gpt-oss-120b"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None=None
    top_k: int=10
    rerank_top_k: int=5
    model_config= SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
settings=Settings()