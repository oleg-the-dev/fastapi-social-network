import os
import secrets

from pydantic import BaseSettings

CWD = os.getcwd()
PARDIR = os.pardir
ENV_FILE_PATH = os.path.abspath(os.path.join(CWD, PARDIR)) + "/.env"


class Settings(BaseSettings):
    # FastAPI
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # Database Admin
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    @property
    def db_string(self):
        return (f"postgresql+psycopg2://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_DB}")


settings = Settings(_env_file=ENV_FILE_PATH)
