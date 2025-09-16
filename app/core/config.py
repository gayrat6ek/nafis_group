
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
import os


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Routes"
    version: str = "1.0.0"


    refresh_token_expire_minutes: int = 60*24*10
    access_token_expire_minutes: int = 60*24*10
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    docs_username: str =os.getenv("DOCS_USERNAME")
    docs_password: str = os.getenv("DOCS_PASSWORD")

    admin_role:str = os.getenv('ADMIN_ROLE')
    admin_password:str = os.getenv('ADMIN_PASSWORD')

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    payme_password: str = os.getenv("PAYME_PASSWORD")
    payme_merchant_id: str = os.getenv("PAYME_MERCHANT_ID")
    playmobile_login: str = os.getenv('PLAYMOBILE_LOGIN')
    playmobile_password: str = os.getenv("PLAYMOBILE_PASSWORD")



    # Security settings


    class Config:
        env_file = ".env"  # Specify the environment file to load


# Initialize settings
settings = Settings()
