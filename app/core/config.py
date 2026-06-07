from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sales Management API"
    API_V1_STR: str = "/api/v1"

    # Berikan default string kosong agar aplikasi tidak crash saat build di Vercel
    # (jika environment variable lupa diset).
    CONNECTION_STRING: str = Field(default="", description="Database connection string")

    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    @property
    def async_database_url(self) -> str:
        if not self.CONNECTION_STRING:
            # Fallback ke in-memory sqlite jika tidak ada env vars
            return "sqlite+aiosqlite:///:memory:"
        if self.CONNECTION_STRING.startswith("postgresql://"):
            return self.CONNECTION_STRING.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.CONNECTION_STRING

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

settings = Settings()
