FILES = 'ABCDEFGH'
RANKS = '12345678'
        
PIECES = {
    'white' : {
        'king' : '♔',
        'queen'	: '♕',
        'rook': '♖',
        'bishop': '♗',
        'knight': '♘',
        'pawn': '♙',
    },
    'black' : {
        'king' : '♚',
        'queen'	: '♛',
        'rook': '♜',
        'bishop': '♝',
        'knight': '♞',
        'pawn': '♟︎',
    }
}

def make_board():
    board = {}
    for col_name in FILES:
        for row_name in RANKS:
            board[col_name + row_name] = None
    return board

def start_board(board):
    board['A1'] = PIECES['white']['rook']
    board['B1'] = PIECES['white']['knight']
    board['C1'] = PIECES['white']['bishop']
    board['D1'] = PIECES['white']['queen']
    board['E1'] = PIECES['white']['king']
    board['F1'] = PIECES['white']['bishop']
    board['G1'] = PIECES['white']['knight']
    board['H1'] = PIECES['white']['rook']
    
    board['A2'] = PIECES['white']['pawn']
    board['B2'] = PIECES['white']['pawn']
    board['C2'] = PIECES['white']['pawn']
    board['D2'] = PIECES['white']['pawn']
    board['E2'] = PIECES['white']['pawn']
    board['F2'] = PIECES['white']['pawn']
    board['G2'] = PIECES['white']['pawn']
    board['H2'] = PIECES['white']['pawn']
    
    
    board['A8'] = PIECES['black']['rook']
    board['B8'] = PIECES['black']['knight']
    board['C8'] = PIECES['black']['bishop']
    board['D8'] = PIECES['black']['queen']
    board['E8'] = PIECES['black']['king']
    board['F8'] = PIECES['black']['bishop']
    board['G8'] = PIECES['black']['knight']
    board['H8'] = PIECES['black']['rook']
    
    board['A7'] = PIECES['black']['pawn']
    board['B7'] = PIECES['black']['pawn']
    board['C7'] = PIECES['black']['pawn']
    board['D7'] = PIECES['black']['pawn']
    board['E7'] = PIECES['black']['pawn']
    board['F7'] = PIECES['black']['pawn']
    board['G7'] = PIECES['black']['pawn']
    board['H7'] = PIECES['black']['pawn']

def board_view(board):
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

def new_game():
    board = make_board()
    start_board(board)
    return board

def run():
    pass

if __name__ == '__main__':
    board = new_game()
    print(board_view(board))