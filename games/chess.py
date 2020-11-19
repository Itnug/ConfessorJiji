pieces = {
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
    for col_name in 'ABCDEFGH':
        for row_name in '12345678':
            board[col_name + row_name] = None
    return board

def start_board(board):
    board['A1'] = pieces['white']['rook']
    board['B1'] = pieces['white']['knight']
    board['C1'] = pieces['white']['bishop']
    board['D1'] = pieces['white']['queen']
    board['E1'] = pieces['white']['king']
    board['F1'] = pieces['white']['bishop']
    board['G1'] = pieces['white']['knight']
    board['H1'] = pieces['white']['rook']
    
    board['A2'] = pieces['white']['pawn']
    board['B2'] = pieces['white']['pawn']
    board['C2'] = pieces['white']['pawn']
    board['D2'] = pieces['white']['pawn']
    board['E2'] = pieces['white']['pawn']
    board['F2'] = pieces['white']['pawn']
    board['G2'] = pieces['white']['pawn']
    board['H2'] = pieces['white']['pawn']
    
    
    board['A8'] = pieces['black']['rook']
    board['B8'] = pieces['black']['knight']
    board['C8'] = pieces['black']['bishop']
    board['D8'] = pieces['black']['queen']
    board['E8'] = pieces['black']['king']
    board['F8'] = pieces['black']['bishop']
    board['G8'] = pieces['black']['knight']
    board['H8'] = pieces['black']['rook']
    
    board['A7'] = pieces['black']['pawn']
    board['B7'] = pieces['black']['pawn']
    board['C7'] = pieces['black']['pawn']
    board['D7'] = pieces['black']['pawn']
    board['E7'] = pieces['black']['pawn']
    board['F7'] = pieces['black']['pawn']
    board['G7'] = pieces['black']['pawn']
    board['H7'] = pieces['black']['pawn']

def board_view(board):
    view = '\n'
    br = '+'+'---+'*8
    view += br + '\n'
    for j in '87654321':
        line = '|'
        for i in 'ABCDEFGH':
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
    view = board_view(board)
    return view

if __name__ == '__main__':
    view = new_game()
    print(view)