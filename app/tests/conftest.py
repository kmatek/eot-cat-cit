import pytest

from flaskr import create_app


@pytest.fixture
def app():
    app = create_app(test_config=True)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
