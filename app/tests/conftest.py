import pytest

from flaskr import create_app
from flaskr.database import db


@pytest.fixture
def app():
    """
    Test client.
    """
    app = create_app(test_config=True)

    # Register database
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    yield app

    # Drop data
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
