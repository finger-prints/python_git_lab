from enum import Enum, auto
import re

INTEGER_MATCH = re.compile(r"[0-9]*")

class GameState(Enum):
    NOT_FINISHED = auto(),
    X_WON = auto(),
    O_WON = auto(),
    TIE = auto()

class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.game_state = GameState.NOT_FINISHED

    def print_board(self):
        for idx, tile in enumerate(self.board):
            print(f" {tile} ", end='')
            if idx % 3 == 2:
                print('\t', end='')
                print(" {} | {} | {} ".format(idx-2, idx-1, idx))
                if idx < len(self.board)-1:
                    print("{dashes}\t{dashes}".format(dashes='-' * 11))
            else: 
                print('|', end='')

    def place_tile(self, character, index):
        self.board[index] = character
    
    def computer_move(self):
        #TODO: make the computer move smarter
        for idx, tile in enumerate(self.board):
            if tile == ' ':
                self.place_tile('O', idx)
                return

    def can_place_move(self, idx):
        #TODO: check if the tile is empty
        return True

    def update_game_state(self):
        #TODO: make this actually do something
        return

    def print_game_summary(self):
        #TODO: print the results
        return
        
    def run(self):

        # main game loop
        while self.game_state == GameState.NOT_FINISHED:

            # print the board
            self.print_board()

            # get player move
            player_move = input('Enter position to place X (q to quit): ')

            # verify player move
            while not INTEGER_MATCH.fullmatch(player_move) or int(player_move) < 0 or int(player_move) > 8 or not self.can_place_move(int(player_move)):
                if player_move.lower() == "q":
                    print("Quitting...")
                    return
                print('Error: Input must be an integer index')
                player_move = input('Enter position to place X: ')
            player_move = int(player_move)
            self.place_tile('X', player_move)

            # computer move
            self.computer_move()

            # update game state
            self.update_game_state()

            # handle game state change
            if self.game_state != GameState.NOT_FINISHED:
                self.print_game_summary()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()