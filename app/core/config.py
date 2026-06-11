from pydantic_settings import BaseSettings # Pydantic-settings reads environment variables from .env file and validates them as typed Python objects

class Settings(BaseSettings):
    app_name: str = "NodeRAG"
    vector_db_url: str
    embeddings_api_key: str
    llm_api_key: str
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()