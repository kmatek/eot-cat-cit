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
    emit('load_game')
    emit('update_credits', {'credits': game_session.get_credit()})


@socketio.on('move')
def on_move(data):
    # Split the data into variables
    row, col = data['position'].split("-")
    game = session['game']

    if 'game_session_id' in session:
        game_session = GameSession.get(session['game_session_id'])

    # Make the move
    game.make_move(int(row), int(col))

    # Check if there is a winner
    if game.check_winner():
        # Increase wins and credits
        game_session.increase_wins()
        game_session.add_credits(4)
        game_session.save()

        emit('update_credits', {'credits': game_session.get_credit()})
        emit('game_over', {'winner': game.check_winner()})
        return

    # Check if there is a draw
    if game.is_draw():
        # Increase draws
        game_session.increase_draws()
        game_session.save()

        emit('game_over', {'draw': True})
        return

    # Make cmoputer move
    row, col = game.make_computer_move()

    # Check if computer is a winner
    if game.check_winner():
        # Increase losses
        game_session.increase_losses()
        game_session.save()

        emit('computer_move', {'position': f'{row}-{col}'})
        emit('game_over', {'winner': game.check_winner(), 'draw': False})
        return

    # Check if there is a draw
    if game.is_draw():
        # Increase draws
        game_session.increase_draws()
        game_session.save()

        emit('computer_move', {'position': f'{row}-{col}'})
        emit('game_over', {'draw': True, 'winner': ''})
        return

    emit('computer_move', {'position': f'{row}-{col}'})


if __name__ == '__main__':
    # Run the application with host, port and debug from app config
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
