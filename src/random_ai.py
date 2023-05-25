from board import Board
import random


class Random:
    @classmethod
    def invoke(cls, board: Board) -> None:
        row = random.randint(0, board.board_width - 1)
        col = random.randint(0, board.board_width - 1)

        index = board.board_position_to_index(row, col)
        board.move(index)
