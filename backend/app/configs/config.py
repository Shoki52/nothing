import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")


class PostgresSettings(BaseSettings):
    PG_USER: str = os.getenv("PG_USER")
    PG_PASSWORD: str = os.getenv("PG_PASSWORD")
    PG_SERVER: str = os.getenv("PG_SERVER")
    PG_DB: str = os.getenv("PG_DB")


class RedisSettings(BaseSettings):
    RD_SERVER: str = os.getenv("RD_SERVER")
    RD_PASSWORD: str = os.getenv("RD_PASSWORD")


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")


class S3Settings(BaseSettings):
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY")
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")
