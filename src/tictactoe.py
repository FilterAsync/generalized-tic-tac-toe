from algorithms import Algorithms
from board import Board, State
from constants import *
from pygame.event import Event
from itertools import product
from typing import Tuple
import pygame, sys


class TicTacToe:
    def __init__(self, board: Board) -> None:
        pygame.init()
        pygame.font.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
        game_icon = pygame.image.load("src\\images\\tictactoe.png").convert()
        pygame.display.set_icon(game_icon)
        self.font = pygame.font.SysFont("Segoe UI", 30, True)

        self.game_board = board
        self.square_size = SCREEN_WIDTH // self.game_board.board_width
        self.offset = self.square_size // 2

        self.ai = 1
        self.play_with_ai = True

    def draw_grid(self) -> None:
        square_size = self.square_size

        for x in range(1, self.game_board.board_width):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, x * square_size),
                (SCREEN_WIDTH, x * square_size),
                LINE_WIDTH,
            )

            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (x * square_size, 0),
                (x * square_size, SCREEN_WIDTH),
                LINE_WIDTH,
            )

    def draw_marker_o(self, row: int, col: int) -> None:
        square_size = self.square_size

        pygame.draw.circle(
            self.screen,
            CIRC_COLOR,
            (
                col * square_size + self.offset,
                row * square_size + self.offset,
            ),
            self.offset // 2,
            CIRC_RADIUS - self.game_board.board_width // 2,
        )

    def draw_marker_x(self, row: int, col: int) -> None:
        square_size = self.square_size
        offset = self.offset // 2

        pygame.draw.line(
            self.screen,
            CROSS_COLOR,
            (col * square_size + offset, row * square_size + offset),
            (col * square_size + offset * 3, row * square_size + offset * 3),
            CROSS_WIDTH,
        )

        pygame.draw.line(
            self.screen,
            CROSS_COLOR,
            (col * square_size + offset, row * square_size + offset * 3),
            (col * square_size + offset * 3, row * square_size + offset),
            CROSS_WIDTH,
        )

    def draw_markers(self) -> None:
        board_width = self.game_board.board_width

        for row, col in product(range(board_width), range(board_width)):
            if self.game_board.board[row][col] == State.O:
                self.draw_marker_o(row, col)

            if self.game_board.board[row][col] == State.X:
                self.draw_marker_x(row, col)

    def draw_winner(self) -> None:
        winner = self.game_board.winner
        text_string = f"{winner.name} wins!"

        if winner == State.Blank:
            text_string = "Draw!"

        text = self.font.render(text_string, True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_WIDTH // 2))

        self.screen.blit(text, text_rect)

    def mouse_position_to_index(self, position: Tuple[int, int]) -> int:
        square_size = self.square_size

        col = position[0] // square_size
        row = position[1] // square_size

        index = self.game_board.board_position_to_index(row, col)

        return index

    def handle_events(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                self.play_with_ai = not self.play_with_ai
                self.game_board.reset()

            if event.key == pygame.K_r:
                self.game_board.reset()

            if event.key == pygame.K_0:
                self.ai = 0
                self.game_board.reset()

            if event.key == pygame.K_1:
                self.ai = 1
                self.game_board.reset()

    def handle_player_move(self, mouse_position: Tuple[int, int]) -> None:
        index = self.mouse_position_to_index(mouse_position)

        if index in range(self.game_board.num_elements):
            self.game_board.move(index)

    def play_move(self, event: Event) -> None:
        if self.play_with_ai and self.game_board.player_turn == State.X:
            if self.ai == 1:
                Algorithms.minimax(self.game_board)
            else:
                Algorithms.random(self.game_board)

            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_player_move(pygame.mouse.get_pos())

    def play(self) -> None:
        while True:
            self.screen.fill(BG_COLOR)
            self.draw_grid()
            self.draw_markers()

            for event in pygame.event.get():
                self.handle_events(event)

                if self.game_board.game_over:
                    continue

                self.play_move(event)

            if self.game_board.game_over:
                self.draw_winner()

            pygame.display.flip()

            self.clock.tick(FPS_LIMIT)
