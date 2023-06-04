from flaskr import create_app

from flaskr.database import db_session, init_db


# Initalize the database
init_db()

app = create_app()
app.db_session = db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    app.db_session.remove()


if __name__ == '__main__':
    # Run the application with host, port and debug from app config
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'])
