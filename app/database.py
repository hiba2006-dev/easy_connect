import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def _build_database_url() -> str:
    # MySQL only: this app is configured to use phpMyAdmin/MySQL stack.
    db_driver = os.getenv("DB_DRIVER", "mysql").lower()
    if db_driver != "mysql":
        raise RuntimeError(
            "Unsupported DB_DRIVER. This project is configured for MySQL only."
        )

    db_user = "root"
    db_password = quote_plus("harbalhiba2006")
    db_host = "localhost"
    db_port = "3306"
    db_name = "easyconnect"

    return (
        f"mysql+pymysql://{db_user}:{db_password}@"
        f"{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    )


SQLALCHEMY_DATABASE_URL = _build_database_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

