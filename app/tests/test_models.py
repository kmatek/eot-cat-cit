from datetime import datetime

from freezegun import freeze_time

from flaskr.models import GameSession


def test_create_game_session(app):
    """Test creating a new game session."""
    with app.app_context():
        game_session = GameSession()
        game_session.create(app.db_session)
        game_session.save(app.db_session)

        assert game_session.id == 1
        assert game_session.credits == 10
        assert game_session.wins == 0
        assert game_session.losses == 0
        assert game_session.draws == 0
        assert game_session.created_at is not None
        assert game_session.ended_at is None


@freeze_time("2023-01-1T10:00:00Z")
def test_create_game_session_methods(app):
    """
    Test the methods of the game session model.
    """
    fake_date = datetime(2023, 1, 1, 10, 0, 0)

    with app.app_context():
        game_session = GameSession(created_at=datetime.utcnow())
        game_session.create(app.db_session)
        game_session.save(app.db_session)

        assert game_session.get_credit() == 10
        assert game_session.get_date_created == fake_date.date()

        game_session.add_credits(10)
        assert game_session.get_credit() == 20

        game_session.substract_credits(10)
        assert game_session.get_credit() == 10

        game_session.increase_wins()
        assert game_session.wins == 1

        game_session.increase_losses()
        assert game_session.losses == 1

        game_session.increase_draws()
        assert game_session.draws == 1

        game_session.start_game_session()
        assert game_session.get_credit() == 7

        game_session.reset_credits()
        assert game_session.get_credit() == 10

        assert game_session.time_played == 0

        freezer = freeze_time("2023-01-1T10:20:00Z")
        freezer.start()

        game_session.close_game_session()
        assert game_session.ended_at is not None
        assert game_session.time_played == 1200

        freezer.stop()


@freeze_time("2023-01-1T10:00:00Z")
def test_create_game_session_get_aggregated_data(app):
    """
    Test the get_aggregated_data method of the game session model.
    """

    response_data = GameSession.get_aggregated_data(
        app.db_session, "2023-01-01")

    assert response_data["total_time_played"] is None
    assert response_data["total_wins"] is None
    assert response_data["total_losses"] is None
    assert response_data["total_draws"] is None

    with app.app_context():
        for i in range(5):
            game_session = GameSession(created_at=datetime.utcnow())
            game_session.create(app.db_session)
            game_session.save(app.db_session)
            game_session.increase_wins()
            game_session.increase_losses()
            game_session.increase_draws()

            freezer = freeze_time("2023-01-1T10:20:00Z")
            freezer.start()

            game_session.close_game_session()

            freezer.stop()

            game_session.save(app.db_session)

        response_data = GameSession.get_aggregated_data(
            app.db_session, "2023-01-01")

        assert response_data["total_time_played"] == 6000
        assert response_data["total_wins"] == 5
        assert response_data["total_losses"] == 5
        assert response_data["total_draws"] == 5

        freezer = freeze_time("2023-01-2T10:00:00Z")
        freezer.start()

        for i in range(2):
            game_session = GameSession(created_at=datetime.utcnow())
            game_session.create(app.db_session)
            game_session.save(app.db_session)
            game_session.increase_wins()
            game_session.increase_losses()
            game_session.increase_draws()

            freezer2 = freeze_time("2023-01-2T10:20:00Z")
            freezer2.start()

            game_session.close_game_session()

            freezer2.stop()

            game_session.save(app.db_session)

        freezer.stop()

        response_data = GameSession.get_aggregated_data(
            app.db_session, "2023-01-02")

        assert response_data["total_time_played"] == 2400
        assert response_data["total_wins"] == 2
        assert response_data["total_losses"] == 2
        assert response_data["total_draws"] == 2
