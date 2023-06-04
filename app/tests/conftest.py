import os

import pytest
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from flaskr import create_app
from flaskr.database import create_db_engine


@pytest.fixture()
def testdb_session():
    """Session for SQLAlchemy."""
    engine = create_db_engine(database_url=os.environ.get('TEST_DATABASE_URL'))
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()

    # Import all modules here that might define models so that
    # they will be registered properly on the metadata.
    from flaskr import models # noqa
    models.Base.metadata.create_all(bind=engine)

    yield db_session

    from flaskr import models
    # Teardown code executed after the test
    db_session.remove()  # Close the session
    engine = db_session.get_bind()
    engine.dispose()  # Disconnect from the database
    models.Base.metadata.drop_all(bind=engine)  # Drop all tables


@pytest.fixture
def app(testdb_session):
    app = create_app(test_config=True)
    app.db_session = testdb_session

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
