from board import Board
from tictactoe import TicTacToe
from typing import List
import sys


def main(args: List[str]) -> None:
    board_width = -1
    num_marks_to_win = -1

    if len(args) > 2:
        try:
            board_width, num_marks_to_win = map(int, args[1:3])

            if board_width < 3 or board_width > 10:
                raise ValueError("Board width should be within [3, 10].")

            if num_marks_to_win < 3 or num_marks_to_win > 10:
                raise ValueError("Number of marks to win should be within [3, 10].")

            if num_marks_to_win > board_width:
                raise ValueError("Number of marks to win must not exceed board width.")

        except (IndexError, ValueError) as e:
            print("Error:", e)
            print("Invalid values found in arguments. Default values will be used.")
    else:
        print("Not enough arguments specified. Default values will be used.")

    if board_width == -1:
        board_width = 3

    if num_marks_to_win == -1:
        num_marks_to_win = 3

    board = Board(board_width, num_marks_to_win)

    tictactoe = TicTacToe(board)
    tictactoe.play()


if __name__ == "__main__":
    main(sys.argv)
