from flaskr.utils import TicTacToe


def test_check_winner():
    game = TicTacToe()
    game.board = [["X", "X", "X"], [" ", " ", " "], [" ", " ", " "]]
    assert game.check_winner() == "X"

    game.board = [[" ", " ", " "], ["X", "X", "X"], [" ", " ", " "]]
    assert game.check_winner() == "X"

    game.board = [[" ", " ", " "], [" ", " ", " "], ["X", "X", "X"]]
    assert game.check_winner() == "X"

    game.board = [["X", " ", " "], ["X", " ", " "], ["X", " ", " "]]
    assert game.check_winner() == "X"

    game.board = [[" ", "X", " "], [" ", "X", " "], [" ", "X", " "]]
    assert game.check_winner() == "X"

    game.board = [[" ", " ", "X"], [" ", " ", "X"], [" ", " ", "X"]]
    assert game.check_winner() == "X"

    game.board = [["X", " ", " "], [" ", "X", " "], [" ", " ", "X"]]
    assert game.check_winner() == "X"

    game.board = [[" ", " ", "X"], [" ", "X", " "], ["X", " ", " "]]
    assert game.check_winner() == "X"

    game.board = [["X", "O", "X"], ["O", "O", "X"], ["X", "X", "O"]]
    assert game.check_winner() is None

    game.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
    assert game.check_winner() is None

    game.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "X"]]
    assert game.check_winner() == "X"

    game.board = [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]]
    assert game.check_winner() == "X"


def test_is_draw():
    game = TicTacToe()
    game.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "X"]]
    assert game.is_draw() is True

    game.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", " "]]
    assert game.is_draw() is False

    game.board = [["X", "O", "X"], ["O", "X", "O"], [" ", " ", " "]]
    assert game.is_draw() is False

    game.board = [["X", "O", "X"], ["O", "X", " "], [" ", " ", " "]]
    assert game.is_draw() is False

    game.board = [["X", "O", "X"], ["O", " ", " "], [" ", " ", " "]]
    assert game.is_draw() is False

    game.board = [["X", "O", " "], ["O", " ", " "], [" ", " ", " "]]
    assert game.is_draw() is False

    game.board = [["X", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    assert game.is_draw() is False

    game.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    assert game.is_draw() is False


def test_make_move():
    game = TicTacToe()
    game.make_move(0, 0)
    assert game.board == [["X", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    game.make_move(1, 1)
    assert game.board == [["X", " ", " "], [" ", "O", " "], [" ", " ", " "]]

    game.make_move(2, 2)

    assert game.board == [["X", " ", " "], [" ", "O", " "], [" ", " ", "X"]]
    assert game.is_draw() is False


def test_make_computer_move():
    game = TicTacToe()
    game.make_move(1, 1)
    assert game.board == [[" ", " ", " "], [" ", "X", " "], [" ", " ", " "]]

    game.make_computer_move()
    assert game.board == [["O", " ", " "], [" ", "X", " "], [" ", " ", " "]]

    game.make_move(0, 2)
    assert game.board == [["O", " ", "X"], [" ", "X", " "], [" ", " ", " "]]

    game.make_computer_move()
    assert game.board == [["O", " ", "X"], [" ", "X", " "], ["O", " ", " "]]

    game.make_move(2, 2)
    assert game.board == [["O", " ", "X"], [" ", "X", " "], ["O", " ", "X"]]

    game.make_computer_move()
    assert game.board == [["O", " ", "X"], ["O", "X", " "], ["O", " ", "X"]]
    assert game.is_draw() is False
    assert game.check_winner() == "O"
