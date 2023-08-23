"""Класс с конфигурациями из переменных окружения"""
# pylint: disable=no-name-in-module,too-few-public-methods
from pydantic import BaseSettings, PostgresDsn, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: PostgresDsn
    graylog_host: str
    compose_project_name: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()  # type: ignore
