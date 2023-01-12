from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(
    settings.db_string
)
session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()


@contextmanager
def db_session():
    with engine.connect() as connection:
        session = session_factory(bind=connection)
        try:
            yield session
        except Exception:
            raise
        finally:
            session.close()
