
white_king = '♔'
white_queen = '♕'
white_rook = '♖'
white_bishop = '♗'
white_knight = '♘'
white_pawn = '♙'

black_king = '♚'
black_queen = '♛'
black_rook = '♜'
black_bishop = '♝'
black_knight = '♞'
black_pawn = '♟︎'

from itertools import count

error_sequence = count(1000,1)

class ErrorCode():
    def __init__(self, description):
        self.code = next(error_sequence)
        self.description = description

InvalidPlayer = ErrorCode('player is not current')

class Chess():

    def __init__(self, whitePlayer, blackPlayer):
        self.players = {
            'white': whitePlayer,
            'black': blackPlayer 
        }

        self._current = 'white'

    def update(self, player, move):
        if self.current_player() != player:
            return InvalidPlayer
        

    def current_player(self):
        return self.players[self._current]

    def toggle_player(self):
        if self._current == 'white':
            self._current = 'black'
        else:
            self._current = 'white'
    
def main(*args, **kwargs):
    Chess('A', 'B')

if __name__ == "__main__":
    main()