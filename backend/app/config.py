import os
from datetime import timedelta
from urllib.parse import quote_plus


def _build_database_url() -> str:
    if explicit := os.environ.get("DATABASE_URL"):
        return explicit
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "3306")
    user = os.environ.get("DB_USER", "inkmill")
    password = quote_plus(os.environ.get("DB_PASSWORD", "inkmill"))
    name = os.environ.get("DB_NAME", "inkmill")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"


class Config:
    database_url: str = _build_database_url()
    jwt_secret: str = os.environ.get("JWT_SECRET", "inkmill-jwt-secret-change-me")
    jwt_algorithm: str = os.environ.get("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

    @property
    def jwt_access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.access_token_expire_minutes)


settings = Config()
