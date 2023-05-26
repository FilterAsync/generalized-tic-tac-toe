from enum import Enum


class State(Enum):
    Blank = ""
    O = "O"
    X = "X"


class Board:
    def __init__(self, board_width: int, num_marks_to_win: int) -> None:
        self.board = [
            [State.Blank for _ in range(board_width)] for _ in range(board_width)
        ]

        self.num_marks_to_win = num_marks_to_win
        self.board_width = board_width
        self.num_elements = board_width * board_width

        self.moves_count = 0
        self.available_moves = set(range(self.num_elements))

        self._game_over = False
        self._player_turn = State.O
        self._winner = State.Blank

    @property
    def game_over(self) -> bool:
        return self._game_over

    @game_over.setter
    def game_over(self, value: bool) -> None:
        self._game_over = value

    @property
    def player_turn(self) -> State:
        return self._player_turn

    @player_turn.setter
    def player_turn(self, state: State) -> None:
        self._player_turn = state

    @property
    def winner(self) -> State:
        if not self.game_over:
            raise RuntimeError("Game is not over yet.")

        return self._winner

    @winner.setter
    def winner(self, state: State) -> None:
        self._winner = state

    def reset(self) -> None:
        self.moves_count = 0
        self.available_moves = set(range(self.num_elements))
        self.game_over = True
        self.player_turn = State.X if self.winner == State.X else State.O
        self.winner = State.Blank
        self.game_over = False
        self.board = [
            [State.Blank for _ in range(self.board_width)]
            for _ in range(self.board_width)
        ]

    def board_position_to_index(self, row: int, col: int) -> int:
        return row * self.board_width + col

    def index_to_board_position(self, index: int) -> tuple[int, int]:
        row = index // self.board_width
        col = index % self.board_width

        return row, col

    def move(self, index: int) -> bool:
        if self.game_over:
            raise RuntimeError("Game is over.")

        row, col = self.index_to_board_position(index)

        if self.board[row][col] != State.Blank:
            return False

        self.board[row][col] = self.player_turn

        self.moves_count += 1
        self.available_moves.remove(index)

        self.check_game_over(row, col)
        self.switch_turn()

        return True

    def check_game_over(self, row: int, col: int) -> None:
        if self.has_player_won(row, col, self.player_turn):
            self.winner = self.player_turn
            self.game_over = True
        elif self.is_board_full():
            self.winner = State.Blank
            self.game_over = True

    def switch_turn(self) -> None:
        self.player_turn = State.X if self.player_turn == State.O else State.O

    def is_board_full(self) -> bool:
        return self.moves_count == self.num_elements

    def has_player_won(self, row: int, col: int, player: State) -> bool:
        if self.moves_count < 2 * self.num_marks_to_win - 1:
            return False

        N = self.board_width

        # check vertical
        count_vertical = 1
        row_up = row - 1

        while row_up >= 0 and self.board[row_up][col] == player:
            count_vertical += 1
            row_up -= 1

        row_down = row + 1
        while row_down < N and self.board[row_down][col] == player:
            count_vertical += 1
            row_down += 1

        if count_vertical >= self.num_marks_to_win:
            return True

        # check horizontal
        count_horizontal = 1
        col_left = col - 1
        while col_left >= 0 and self.board[row][col_left] == player:
            count_horizontal += 1
            col_left -= 1

        col_right = col + 1
        while col_right < N and self.board[row][col_right] == player:
            count_horizontal += 1
            col_right += 1

        if count_horizontal >= self.num_marks_to_win:
            return True

        # check diagonals
        count_diagonal_left = 1
        row_left_up = row - 1
        col_left_up = col - 1
        while (
            row_left_up >= 0
            and col_left_up >= 0
            and self.board[row_left_up][col_left_up] == player
        ):
            count_diagonal_left += 1
            row_left_up -= 1
            col_left_up -= 1

        row_right_down = row + 1
        col_right_down = col + 1

        while (
            row_right_down < N
            and col_right_down < N
            and self.board[row_right_down][col_right_down] == player
        ):
            count_diagonal_left += 1
            row_right_down += 1
            col_right_down += 1

        count_diagonal_right = 1
        row_left_down = row + 1
        col_left_down = col - 1
        while (
            row_left_down < N
            and col_left_down >= 0
            and self.board[row_left_down][col_left_down] == player
        ):
            count_diagonal_right += 1
            row_left_down += 1
            col_left_down -= 1

        row_right_up = row - 1
        col_right_up = col + 1
        while (
            row_right_up >= 0
            and col_right_up < N
            and self.board[row_right_up][col_right_up] == player
        ):
            count_diagonal_right += 1
            row_right_up -= 1
            col_right_up += 1

        if (
            count_diagonal_left >= self.num_marks_to_win
            or count_diagonal_right >= self.num_marks_to_win
        ):
            return True

        return False

    def deepcopy(self):
        new_board = Board(self.board_width, self.num_marks_to_win)

        new_board.board = [row.copy() for row in self.board]
        new_board.player_turn = self._player_turn
        new_board.winner = self._winner
        new_board.available_moves = self.available_moves.copy()
        new_board.game_over = self._game_over
        new_board.moves_count = self.moves_count

        return new_board
