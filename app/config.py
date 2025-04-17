import dataclasses

from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    host: str
    port: int
    db: int
    user: str
    password: str

    class Config:
        env_prefix = "db_"
        env_file = ".env"
        env_file_encoding = "utf-8"


class CiphersSettings(BaseSettings):
    salt: str

    class Config:
        env_prefix = "cipher_"
        env_file = ".env"
        env_file_encoding = "utf-8"


class JWTSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    class Config:
        env_prefix = "jwt_"
        env_file = ".env"
        env_file_encoding = "utf-8"


@dataclasses.dataclass
class Settings:
    db_settings: DBSettings = DBSettings()
    cipher_settings: CiphersSettings = CiphersSettings()


settings = Settings()
