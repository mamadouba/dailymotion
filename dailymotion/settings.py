from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    log_level: Optional[str] = "DEBUG"

    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str

    redis_host: Optional[str] = "localhost"
    redis_port: Optional[str] = "6379"

    smtp_host: Optional[str] = "localhost"
    smtp_port: Optional[str] = "1025"
    smtp_sender: Optional[str] = "noreply@test.dev"

    user_activation_code_validity: Optional[str] = "1"

    @property
    def debug(cls):
        return cls.log_level.lower() == "debug"

    @property
    def db_uri(cls):
        return f"postgresql://{cls.db_user}:{cls.db_password}@{cls.db_host}:{cls.db_port}/{cls.db_name}"

    @property
    def redis_uri(cls):
        return f"redis://{cls.redis_host}:{cls.redis_port}/0?encoding=utf-8"

    @property
    def user_activation_code_expires(cls):
        return int(cls.user_activation_code_validity) * 60


settings = Settings()
