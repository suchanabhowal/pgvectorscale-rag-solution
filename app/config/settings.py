"""import logging
import os
from datetime import timedelta
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(dotenv_path="./.env")


def setup_logging():
    #Configure basic logging for the application.
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


class LLMSettings(BaseModel):
    #Base settings for Language Model configurations.

    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3


class OpenAISettings(LLMSettings):
    #OpenAI-specific settings extending LLMSettings.

    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    default_model: str = Field(default="gpt-4o")
    embedding_model: str = Field(default="text-embedding-3-small") 

from pydantic import Field
import os

class HuggingFaceSettings(LLMSettings):
    #Hugging Face-specific settings extending LLMSettings.

    model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    cache_dir: str = Field(default_factory=lambda: os.getenv("HF_CACHE_DIR", "./hf_cache"))


class DatabaseSettings(BaseModel):
    #Database connection settings.

    service_url: str = Field(default_factory=lambda: os.getenv("TIMESCALE_SERVICE_URL"))


class VectorStoreSettings(BaseModel):
    #Settings for the VectorStore.

    table_name: str = "embeddings_1"
    embedding_dimensions: int = 1536
    time_partition_interval: timedelta = timedelta(days=7)


class Settings(BaseModel):
    #Main settings class combining all sub-settings.

    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)

@lru_cache()
def get_settings() -> Settings:
    #Create and return a cached instance of the Settings.
    settings = Settings()
    setup_logging()
    return settings """



import logging
import os
from datetime import timedelta
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

dotenv_path = r"D:\INFOSYS\pgvectorscale-rag-solution\pgvectorscale-rag-solution\app\.env"
load_dotenv(dotenv_path=dotenv_path)


def setup_logging():
    """Configure basic logging for the application."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


class LLMSettings(BaseModel):
    """Base settings for Language Model configurations."""

    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3


class HuggingFaceSettings(LLMSettings):
    """Hugging Face-specific settings extending LLMSettings."""

    model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    cache_dir: str = Field(default_factory=lambda: os.getenv("HF_CACHE_DIR", "./hf_cache"))


"""class DatabaseSettings(BaseModel):
    #Database connection settings.

    service_url: str = Field(default_factory=lambda: os.getenv("TIMESCALE_SERVICE_URL")) """

class DatabaseSettings(BaseModel):
    """Database connection settings."""

    database: str = Field(default_factory=lambda: os.getenv("DATABASE", "postgres"))
    user: str = Field(default_factory=lambda: os.getenv("USER", "postgres"))
    password: str = Field(default_factory=lambda: os.getenv("PASSWORD", "suchana"))
    host: str = Field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    port: int = Field(default_factory=lambda: int(os.getenv("PORT", 5432)))
    service_url: str = Field(default_factory=lambda: os.getenv("TIMESCALE_SERVICE_URL"))

class VectorStoreSettings(BaseModel):
    """Settings for the VectorStore."""

    table_name: str = "embeddings_1"
    embedding_dimensions: int = 1536
    time_partition_interval: timedelta = timedelta(days=7)


class Settings(BaseModel):
    """Main settings class combining all sub-settings."""

    huggingface: HuggingFaceSettings = Field(default_factory=HuggingFaceSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)


@lru_cache()
def get_settings() -> Settings:
    """Create and return a cached instance of the Settings."""
    settings = Settings()
    setup_logging()
    return settings

"""if __name__ == "__main__":
    # Instantiate settings and print a key value to verify the configuration
    settings = get_settings()
    print("HuggingFace Model Name:", settings.huggingface.model_name)
    print("Database Service URL:", settings.database.service_url) """


import psycopg2

if __name__ == "__main__":
    # Instantiate settings
    settings = get_settings()
    
    print("HuggingFace Model Name:", settings.huggingface.model_name)
    print("Database Service URL:", settings.database.service_url)

    # Test database connection
    try:
        conn = psycopg2.connect(
            host=settings.database.host,
            dbname=settings.database.database,
            user=settings.database.user,
            password=settings.database.password,
            port=settings.database.port
        )
        print("Database connection established successfully!")
        conn.close()
    except Exception as error:
        print(f"Error connecting to the database: {error}")
