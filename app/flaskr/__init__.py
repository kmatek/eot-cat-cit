import os

from flask import Flask


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_object('flaskr.config.Config')
    else:
        # Load the test config if passed in
        app.config.from_object('flaskr.config.TestingConfig')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # S simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
