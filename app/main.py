from flask_socketio import SocketIO, emit
from flask_migrate import Migrate
from flask import session
from flask_session import Session

from flaskr import create_app
from flaskr.database import db
from flaskr.utils import TicTacToe
from flaskr.models import GameSession


# Create the application
app = create_app()
socketio = SocketIO(app)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)


# SocketIO event handlers
@socketio.on('connect')
def on_connect():
    print('Someone connected!')


@socketio.on('disconnect')
def on_disconnect():
    print('Someone disconnected!')
    if 'game_session_id' in session:
        game_session = GameSession.get(session['game_session_id'])
        game_session.close_game_session()
        game_session.save()

    session.clear()


@socketio.on('start_game')
def on_start_game():
    """
    Handle the start_game event from SocketIO.
    """
    game = TicTacToe()
    game_session = GameSession()
    game_session.create()
    game_session.save()
    session['game_session_id'] = game_session.id
    session['game'] = game

    game_session.start_game_session()
    game_session.save()
    emit('load_game', {'credits': game_session.get_credit()})


if __name__ == '__main__':
    # Run the application with host, port and debug from app config
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
