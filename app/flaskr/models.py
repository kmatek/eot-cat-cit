from datetime import datetime

from sqlalchemy import Integer, func, exc, cast
from sqlalchemy.types import Date
from sqlalchemy.ext.hybrid import hybrid_property

from .database import db


class GameSession(db.Model):
    __tablename__ = 'game_session'

    id = db.Column(db.Integer, primary_key=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, default=None, nullable=True)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    credits = db.Column(db.Integer, default=10)

    def __repr__(self):
        return f'<GameSession {self.id}>'

    def create(self):
        """
        Create a new game session.
        """
        db.session.add(self)

    def save(self):
        """
        Save the game session.
        """
        db.session.commit()

    def add_credits(self, amount):
        """
        Add credits to the game session.
        """
        self.credits += amount

    def substract_credits(self, amount):
        """
        Substract credits from the game session.
        """
        self.credits -= amount

    def get_credit(self):
        """
        Get the current credits of the game session.
        """
        return self.credits

    def increase_wins(self):
        """
        Increase the wins of the game session.
        """
        self.wins += 1

    def increase_losses(self):
        """
        Increase the losses of the game session.
        """
        self.losses += 1

    def increase_draws(self):
        """
        Increase the draws of the game session.
        """
        self.draws += 1

    @hybrid_property
    def get_date_created(self):
        """
        Get the date created of the game session.
        """
        return self.created_at.date()

    @get_date_created.expression
    def get_date_created(cls):
        return cast(cls.created_at, Date)

    @hybrid_property
    def time_played(self):
        """
        Get the time played of the game session.
        """
        if self.ended_at is None:
            return 0
        return (self.ended_at - self.created_at).seconds

    @time_played.expression
    def time_played(cls):
        """
        SQLAlchemy expression for the time_played property.
        """
        return cast(
            func.coalesce(
                func.extract('epoch', cls.ended_at)
                - func.extract('epoch', cls.created_at), 0
            ),
            Integer
        )

    def reset_credits(self):
        """
        Reset the credits of the game session.
        """
        self.credits = 10

    def close_game_session(self):
        """
        Close the game session.
        """
        self.ended_at = datetime.utcnow()

    def start_game_session(self):
        """
        Start the game session.
        """
        self.substract_credits(3)

    @classmethod
    def get_aggregated_data(cls, date):
        """
        Get the aggregated data of the game session filtered by given date.
        """
        try:
            data = db.session.query(
                func.sum(cls.wins).label('total_wins'),
                func.sum(cls.losses).label('total_losses'),
                func.sum(cls.draws).label('total_draws'),
                func.sum(cls.time_played).label('total_time_played'),
            ).filter(
                cls.get_date_created == date
            ).first()
        except exc.DataError:
            raise exc.DataError('Invalid date format.')

        return data._asdict()

    @classmethod
    def get(cls, id):
        """
        Get the game session by given id.
        """
        return db.get_or_404(cls, id)


def end_game_session(game_session: GameSession):
    """
    End the game session.
    """
    game_session.close_game_session()
    game_session.save()
