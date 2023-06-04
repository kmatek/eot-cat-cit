from flask_socketio import SocketIO
from flask_migrate import Migrate

from flaskr import create_app
from flaskr.database import db


# Create the application
app = create_app()
socketio = SocketIO(app)
# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)


# SocketIO event handlers
@socketio.on('connect')
def on_connect():
    print('Someone connected!')


if __name__ == '__main__':
    # Run the application with host, port and debug from app config
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
