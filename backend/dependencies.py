from typing import Generator

from sqlmodel import create_engine, Session

from config import settings

engine = create_engine(
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


def get_db() -> Generator:
    with Session(engine) as session:
        yield session
