from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345@localhost/delivery_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)


Base = declarative_base()
session = sessionmaker()
