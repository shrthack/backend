from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_host: str = ""
    app_port: int = 0
    db_user: str = ""
    db_name: str = ""
    db_pass: str = ""
    db_host: str = ""
    db_port: int = 0
    jwt_secret: str = ""

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
