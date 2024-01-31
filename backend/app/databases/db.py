from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app.configs.config import PostgresSettings

postgresSettings = PostgresSettings()

# Путь к PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql://{postgresSettings.PG_USER}:{postgresSettings.PG_PASSWORD}@" \
                          f"{postgresSettings.PG_SERVER}/{postgresSettings.PG_DB}"

# Движок
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Если нет базы данных, то создать
if not database_exists(engine.url):
    create_database(engine.url)

# Открытие сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Подключение к PostgreSQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
