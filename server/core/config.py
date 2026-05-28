from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    ACCESS_TOKEN_EXPIRE_MINS : int = 15
    ACCESS_TOKEN_EXPIRE_DAYS : int = 28
    JWT_SECRET : str
    JWL_ALGORITHM : str

    model_config = SettingsConfigDict(env_file=".env.local")


settings = Settings()