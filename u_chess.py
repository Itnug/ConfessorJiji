import re

FILES = 'ABCDEFGH'
RANKS = '12345678'

_piece = '[KQBNR]'
_check = '[+#]'
_rank = '[1-8]'
_file = '[a-h]'

_promotion = f'x?{_file}[18]=(?!K){_piece}'
_pawnmove = f'(?:{_file}?x)?{_file}(?![18]){_rank}'
_stdmove = f'{_piece}{_file}?{_rank}?x?{_file}{_rank}'
_castling = 'O-O(?:-O)?'

_notation = f'({_promotion}|{_castling}|{_pawnmove}|{_stdmove}){_check}?'

PIECES_IN_START_ORDER = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']


PIECES = {
    'white': {
        'king': '♔',
        'queen'	: '♕',
        'rook': '♖',
        'bishop': '♗',
        'knight': '♘',
        'pawn': '♙',
    },
    'black': {
        'king': '♚',
        'queen'	: '♛',
        'rook': '♜',
        'bishop': '♝',
        'knight': '♞',
        'pawn': '♟︎',
    }
}


def make_board():
    rows, cols = (8, 8)
    board = [[None]*cols]*rows

def start_board(board):
    

def build_view(board):
    view = '\n'
    br = '+'+'---+'*8
    view += br + '\n'
    for j in RANKS[::-1]:
        line = '|'
        for i in FILES:
            position = i + j
            if board[position]:
                sprite = board[position]
            else:
                sprite = ' '
            line += ' ' + sprite + ' |'
        view += line + '\n'
        view += br + '\n'
    return view


def is_piece_valid(move):
    if(re.search(_piece, move[0]) or re.search(_file, move[0])):
        return False
    else:
        return True


def new_game():
    board = make_board()
    start_board(board)
    return board


if __name__ == '__main__':
    board = new_game()
    game_over = False
    print(build_view(board))
    while(not(game_over)):
        move = input("Enter a valid move:")
        game_over = is_piece_valid(move)
