from board import Board
from minimax import Minimax
from random_ai import Random


class Algorithms:
    @classmethod
    def random(cls, board: Board) -> None:
        Random.invoke(board)

    @classmethod
    def minimax(cls, board: Board) -> None:
        Minimax.invoke(board, board.player_turn, 4)
