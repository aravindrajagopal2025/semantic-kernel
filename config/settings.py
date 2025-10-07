from typing import Optional
from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    def __init__(self) -> None:
        # override signature so linter sees no required __init__ args
        super().__init__()

    # Kafka/Event Hub - using lowercase fields but accepting both case variants
    kafka_bootstrap_servers: str = Field(
        ...,
        description="e.g. pkc-l7oop.us-west1.gcp.confluent.cloud:9092",
    )
    kafka_username: str = Field(...)
    kafka_password: str = Field(...)

    # AidBox - using lowercase fields but accepting both case variants
    aidbox_base_url: HttpUrl = Field(...)
    aidbox_token: str = Field(...)
    aidbox_username: str = Field(...)
    aidbox_password: str = Field(...)

    # Orchestrator topics & groups - using lowercase fields
    orchestrator_kafka_topic: str = Field(...)
    orchestrator_kafka_callback_topic: str = Field(...)
    orchestrator_kafka_output_success: str = Field(...)
    orchestrator_kafka_output_failure: str = Field(...)
    orchestrator_kafka_group_id: str = Field(...)

    # Mapper topics & groups - using lowercase fields
    mapper_kafka_topic: str = Field(...)
    mapper_kafka_callback_topic: str = Field(...)
    mapper_kafka_group_id: str = Field(...)

    # LLM topics & groups - using lowercase fields
    llm_kafka_topic: str = Field(...)
    llm_kafka_callback_topic: str = Field(...)
    llm_kafka_group_id: str = Field(...)

    # MongoDB for status tracking - using lowercase fields
    mongo_uri: str = Field(...)
    mongo_db: str = Field(...)
    mongo_collection: str = Field(...)

    # Semantic Kernel / Azure OpenAI - using lowercase fields
    azure_openai_key: str = Field(...)
    azure_openai_endpoint: HttpUrl = Field(...)
    azure_openai_model: str = Field(...)
    azure_openai_api_version: str = Field(...)

    # LLM Agent settings
    is_step_by_step_enabled: bool = Field(
        False, description="Enable bulk prompt processing for LLM Agent"
    )
    results_dir: str = Field(...)

    # Retry logic - using lowercase fields
    max_agent_retries: int = Field(2)

    # Azure Blob Storage - using lowercase fields
    azure_blob_connection_string: str = Field(...)
    azure_blob_mapper_agent_container: str = Field(...)
    azure_blob_llm_agent_container: str = Field(...)

    # Azure Document Intelligence (Optional)
    azure_di_api_key: Optional[str] = Field(
        None, description="Azure Document Intelligence API Key"
    )
    azure_di_document_intelligence_endpoint: Optional[HttpUrl] = Field(
        None, description="Azure Document Intelligence Endpoint"
    )
    azure_di_default_model: str = Field(
        "prebuilt-layout", description="Default model for Document Intelligence"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,  # This allows both uppercase and lowercase env vars
    )

    @field_validator("*", mode="before")
    def _no_empty_str(cls, v):
        # catch any str that’s all whitespace (or zero‐length)
        if isinstance(v, str) and not v.strip():
            raise ValueError("must be set and non‑empty")
        return v


# Now no linter errors or warnings here:
settings = Settings()
