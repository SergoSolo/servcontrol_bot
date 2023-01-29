import logging

from aiogram import Bot
from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


logger = logging.getLogger(__name__)


def logger_config():
    logging.basicConfig(
        datefmt="%d.%m.%Y %H:%M:%S",
        format="%(asctime)s, %(levelname)s, %(message)s",
        level=logging.INFO,
    )


settings = Settings()
bot = Bot(token=settings.BOT_TOKEN)
