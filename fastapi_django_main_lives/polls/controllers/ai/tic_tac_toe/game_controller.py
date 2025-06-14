from tic_tac_toe.game import GameBoard, Player

class GameController:
    def __init__(self):
        self.board = GameBoard()
        self.current_player = Player.X

    def play_game(self):
        while True:
            self.board.print_board()
            row = int(input("Enter row: "))
            col = int(input("Enter column: "))
            if self.board.make_move(row, col, self.current_player):
                if self.board.check_win(self.current_player):
                    self.board.print_board()
                    print(f"Player {self.current_player.name} wins!")
                    break
                elif self.board.is_draw():
                    self.board.print_board()
                    print("It's a draw!")
                    break
                self.current_player = Player.O if self.current_player == Player.X else Player.X
            else:
                print("Invalid move, try again.")