from pydantic_settings import (
    BaseSettings,
)  # Pydantic-settings reads environment variables from .env file and validates them as typed Python objects


class Settings(BaseSettings):
    app_name: str = "NodeRAG"
    environment: str = "development"
    opensearch_url: str
    opensearch_index_name: str = "noderag_vectors"
    embeddings_api_key: str = ""
    llm_api_key: str = ""
    llm_model_name: str = ""
    max_file_size_mb: int = 10
    allowed_file_types: str = "pdf, txt, docx"

    class Config:
        env_file = ".env"


settings = Settings()
