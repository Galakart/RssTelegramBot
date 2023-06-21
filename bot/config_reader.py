from pydantic import BaseSettings, PostgresDsn, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: PostgresDsn
    graylog_host: str
    compose_project_name: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
