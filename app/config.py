from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Class for creating URL for DB using file .env"""

    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int

    SECRET_KEY: str
    ALGORITM: str


    @property
    def get_db_url(self):
        return (
            f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
            )
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

