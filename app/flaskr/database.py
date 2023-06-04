import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


def create_db_engine(database_url: str):
    return create_engine(database_url)


engine = create_db_engine(database_url=os.environ.get('DATABASE_URL'))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # Import all modules here that might define models so that
    # they will be registered properly on the metadata.
    from flaskr import models
    models.Base.metadata.create_all(bind=engine)
