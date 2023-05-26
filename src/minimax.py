# TODO: optimize further minimax

from board import Board, State
from math import inf


class Minimax:
    @classmethod
    def invoke(cls, board: Board, player: State, max_depth: int) -> None:
        if max_depth <= 0:
            raise ValueError("Maximum depth must be greater than 0.")

        cls.max_depth = max_depth
        cls.minimax(board, player, 0, -inf, inf)

    @classmethod
    def minimax(
        cls,
        board: Board,
        player: State,
        depth: int,
        alpha: float,
        beta: float,
    ) -> float:
        if depth == cls.max_depth or board.game_over:
            return cls.score(board, player)

        depth += 1

        if board.player_turn == player:
            return cls.maximize(board, player, depth, alpha, beta)
        else:
            return cls.minimize(board, player, depth, alpha, beta)

    @classmethod
    def maximize(
        cls, board: Board, player: State, depth: int, alpha: float, beta: float
    ) -> float:
        best_move = -1

        for the_move in board.available_moves:
            temp_board = board.deepcopy()
            temp_board.move(the_move)

            score = cls.minimax(temp_board, player, depth, alpha, beta)
            if score > alpha:
                alpha = score
                best_move = the_move

            if alpha >= beta:
                break

        if best_move != -1:
            board.move(best_move)

        return alpha

    @classmethod
    def minimize(
        cls, board: Board, player: State, depth: int, alpha: float, beta: float
    ) -> float:
        best_move = -1

        for the_move in board.available_moves:
            temp_board = board.deepcopy()
            temp_board.move(the_move)

            score = cls.minimax(temp_board, player, depth, alpha, beta)

            if score < beta:
                beta = score
                best_move = the_move

            if alpha >= beta:
                break

        if best_move != -1:
            board.move(best_move)

        return beta

    @classmethod
    def score(cls, board: Board, player: State) -> int:
        if player == State.Blank:
            raise ValueError("Player must be O or X.")

        opponent = State.X if player == State.O else State.O

        if board.game_over and board.winner == player:
            return +1

        if board.game_over and board.winner == opponent:
            return -1

        return 0
