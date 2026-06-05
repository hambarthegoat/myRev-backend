from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sales Management API"
    API_V1_STR: str = "/api/v1"
    
    CONNECTION_STRING: str = Field(..., description="Database connection string")

    @property
    def async_database_url(self) -> str:
        if self.CONNECTION_STRING.startswith("postgresql://"):
            return self.CONNECTION_STRING.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.CONNECTION_STRING

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

settings = Settings()
