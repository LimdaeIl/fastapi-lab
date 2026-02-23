from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parents[4]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        # extra="ignore",  # 보통은 전체 필드를 다 정의하면 필요 없음
    )

    app_env: str = "local"
    app_name: str = "fastapi-lab"
    app_debug: bool = False

    mysql_host: str = "localhost"
    mysql_port: int = 3307
    mysql_db: str = "myapp"
    mysql_user: str = "myapp"
    mysql_password: str = Field(..., description="Required")

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    jwt_secret_key: str = Field(..., min_length=32)
    jwt_access_expires_min: int = 30
    jwt_refresh_expires_days: int = 14
    jwt_algorithm: str = "HS256"

    @property
    def mysql_dsn(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        )

    @property
    def redis_dsn(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


settings = Settings()
