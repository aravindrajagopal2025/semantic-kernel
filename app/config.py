from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow", case_sensitive=False
    )

    azure_openai_endpoint: str
    azure_openai_key: str
    azure_openai_model: str
    azure_openai_api_version: str


settings = Settings()
