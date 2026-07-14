from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "AI Knowledge Assistant"

    DEBUG: bool = True

    GROQ_API_KEY: str | None = None

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()