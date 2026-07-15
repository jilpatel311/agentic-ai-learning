from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "AI Knowledge Assistant"

    DEBUG: bool = True

    GROQ_API_KEY: str | None = None

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # MCP_PORT: int = 8001
    DB_HOST: str = "localhost"

    DB_PORT: int = 3306

    DB_USERNAME: str

    DB_PASSWORD: str

    DB_NAME: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()