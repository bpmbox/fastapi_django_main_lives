from dataclasses import dataclass
from enum import Enum

class Player(Enum):
    X = 1
    O = 2

@dataclass
class GameBoard:
    board: list[list[str]]

    def __post_init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def print_board(self):
        for row in self.board:
            print(' | '.join(row))
            print('---------')

    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = 'X' if player == Player.X else 'O'
            return True
        return False

    def check_win(self, player):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

    def is_draw(self):
        return all(cell != ' ' for row in self.board for cell in row)