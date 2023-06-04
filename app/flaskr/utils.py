def check_draw(lst: list) -> bool:
    """
    Helper function for checking draw.
    """
    for item in lst:
        # Iterate through nested list
        if isinstance(item, list):
            if not check_draw(item):
                return False
        elif item == " ":
            return False
    return True


def get_available_moves(lst: list, parent_index: int = -1) -> list[tuple]:
    """
    Helper function to get availbale place for computer move.
    """
    moves = []
    for index, item in enumerate(lst):
        # Iterate through nested list
        if isinstance(item, list):
            child_indices = get_available_moves(item, index)
            moves.extend(child_indices)
        elif item == " ":
            moves.append((parent_index, index))
    return moves


class TicTacToe:
    def __init__(self):
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.current_player = 'X'

    def check_winner(self):
        """
        Check if there is a winner on the board.
        :param board: 2D list of strings representing the board
        """
        # Check hiorizontal
        if self.board[0][0] == self.board[0][1] == self.board[0][2] != " ":
            return self.board[0][0]
        if self.board[1][0] == self.board[1][1] == self.board[1][2] != " ":
            return self.board[1][0]
        if self.board[2][0] == self.board[2][1] == self.board[2][2] != " ":
            return self.board[2][0]

        # Check vertical
        if self.board[0][0] == self.board[1][0] == self.board[2][0] != " ":
            return self.board[0][0]
        if self.board[0][1] == self.board[1][1] == self.board[2][1] != " ":
            return self.board[0][1]
        if self.board[0][2] == self.board[1][2] == self.board[2][2] != " ":
            return self.board[0][2]

        # Check diagonal
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]

        return None

    def is_draw(self):
        """
        Check if the game is a draw.
        """
        return check_draw(self.board)

    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move on the board.
        :param row: row to make move
        :param col: column to make move
        :return: True if move was made, False otherwise
        """
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def evaluate(self):
        winner = self.check_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        else:
            return 0

    def minimax(self, depth, maximizing_player):
        if self.check_winner() is not None:
            return self.evaluate()

        if self.is_draw():
            return 0

        if maximizing_player:
            max_eval = float("-inf")
            for move in get_available_moves(self.board):
                self.board[move[0]][move[1]] = "O"
                eval = self.minimax(depth + 1, False)
                self.board[move[0]][move[1]] = " "
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for move in get_available_moves(self.board):
                self.board[move[0]][move[1]] = "X"
                eval = self.minimax(depth + 1, True)
                self.board[move[0]][move[1]] = " "
                min_eval = min(min_eval, eval)
            return min_eval

    def make_computer_move(self):
        """
        Get the best move for the computer.
        """
        best_score = float("-inf")
        best_move = None
        for move in get_available_moves(self.board):
            self.board[move[0]][move[1]] = "O"
            score = self.minimax(0, False)
            self.board[move[0]][move[1]] = " "
            if score > best_score:
                best_score = score
                best_move = move

        return self.make_move(best_move[0], best_move[1])

    def reset(self):
        """
        Reset the game.
        """
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.current_player = 'X'
