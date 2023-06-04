from flask_socketio import SocketIO

from flaskr import create_app
from flaskr.database import db_session, init_db


# Initalize the database
init_db()

# Create the application
app = create_app()
app.db_session = db_session
socketio = SocketIO(app)


# SocketIO event handlers
@socketio.on('connect')
def on_connect():
    print('Someone connected!')


@app.teardown_appcontext
def shutdown_session(exception=None):
    app.db_session.remove()


if __name__ == '__main__':
    # Run the application with host, port and debug from app config
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
