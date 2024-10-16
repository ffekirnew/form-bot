from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "prod"

    bot_name: str
    bot_token: SecretStr
    webhook_url: str
