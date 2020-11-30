import re

from collections import namedtuple

Sprite = namedtuple('Sprite', ('name', 'id', 'view'))
sprites = [
    Sprite('white_king', 'wK', '♔'),
    Sprite('white_queen', 'wQ', '♕'),
    Sprite('white_rook', 'wR', '♖'),
    Sprite('white_bishop', 'wB', '♗'),
    Sprite('white_knight', 'wN', '♘'),
    Sprite('white_pawn', 'w', '♙'),

    Sprite('black_king', 'bK', '♚'),
    Sprite('black_queen', 'bQ', '♛'),
    Sprite('black_rook', 'bR', '♜'),
    Sprite('black_bishop', 'bB', '♝'),
    Sprite('black_knight', 'bN', '♞'),
    Sprite('black_pawn', 'b', '♟︎'),

    Sprite('h_break', '-', '〰'),
    Sprite('empty_space', ' ', '　') #unicode space - extra wide
]

_piece = '[KQBNR]'
_check = '[+#]'
_rank = '[1-8]'
_file = '[a-h]'

sprites_memo = {}
def sprite_by_name(name):
    if name in sprites_memo:
        return sprites_memo[name]

    for sprite in sprites:
        if sprite.name == name or sprite.id == name:
            sprites_memo[name] = sprite
            return sprite
    raise ValueError('no sprite exists for name = ' + name)

class Board():
    
    def __init__(self, iterable):
        self.model = list(iterable)
        if len(self.model) != 64:
            raise ValueError(f"chess boards have 64 squares genius. {len(self.model)} != 64")

    def __setitem__(self, key, newValue):
        if isinstance(key, str):
            _index = Board.toIndex(key)
            self.model[_index] = sprite_by_name(newValue).id

    def __getitem__(self, key):
        if isinstance(key, str):
            _index = Board.toIndex(key)
            return self.model[_index]

        return self.model.__getitem__(key)

    def __eq__(self, other):
        return isinstance(other, Board) and list(self) == list(other)

    @staticmethod
    def toIndex(a1h8):
        """
        convert a1 to 0, h8 to 63 and everything in between 
        """
        if a1h8[0].lower() not in 'abcdefgh' \
                or a1h8[1] not in '12345678':
            raise ValueError(f'invalid address: {a1h8}')

        _file = 'abcdefgh'.index(a1h8[0].lower())
        _rank = '12345678'.index(a1h8[1])
        return _rank*8 + _file

class BoardView():
    def __init__(self, board):
        self.board = board
        self.isFlipped = False
    
    def _flip(self, iterable):
        if self.isFlipped:
            return reversed(iterable)
        else: 
            return iterable
        
    def __str__(self):
        h_break = sprite_by_name('-').view
        empty_space = sprite_by_name(' ').view
        break_line = '  ' + '+'.join(['']+[f' {h_break} '] * 8 +['']) + '\n'
        view_ranks = []
        
        rank_range = self._flip(range(8))
        file_range = self._flip('ABCDEFGH') 
        
        for i in rank_range:
            spot_range = self._flip(self.board[(7-i)*8:(7-i)*8+8])
            rank_items = map(lambda x: f' {sprite_by_name(x).view} ', spot_range)
            view_ranks.append(f'{str(8-i)} ' + '|'.join(['',*rank_items,'']) + '\n')

        view = break_line.join(['', *view_ranks, ''])
        view += f'   {empty_space}' + f'{empty_space}  '.join(file_range)
        return view

class BoardFactory():
    
    def __init(self):
        pass
    
    def build(self, spec):
        if not spec:
            return self.full()

        if spec.upper() == 'EMPTY':
            return self.empty()
        else:
            return self.full()
    
    def empty(self):
        board = Board(map(lambda x: x.id, [sprite_by_name(' ')]*64))
        return board

    def full(self):
        board = Board([
            'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR',
            *(['w']*8),
            *([' ']*32),
            *(['b']*8),
            'bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'
        ])
        return board

BOARD_FACTORY = BoardFactory()

InvalidPlayer = Exception('player is not current')
InvalidMove = Exception('cannot parse move')

class Move():
    
    def __init__(self, move):
        self.move = move
        self.castling = move in ('O-O','O-O-O')
        if not self.castling:
            self.piece = None
    
    def __str__(self):
        return f'{self.move} = [castling = {self.castling or None}, ' \
            + f'check = {self.check}, ' \
            + f'piece = {self.piece}, ' \
            + f'target_spot = {self.target_spot} ]'

    def parse(self):
        move = self.move 
        
        if move[-1] in '+#':
            self.check = move[-1]
            move = move[:-1]

        if move[0] in 'KQRBN':
            self.piece = move[0]
            move = move[1:] 
        else:
            self.piece = ''
        
        if 'x' in move:
            self.capture = True
            move = move.replace('x','', 1)
        
        self.target_spot = move[-2:]
        move = move[:-2]
        if len(move) == 1:
            self.disambig_src = move
        else:
            return InvalidMove 

def is_pawn_move(move):
    if re.match(f'(?:{_file}x)?{_file}{_rank}', move):
        return True
    return False
    
class ChessEngine():

    def __init__(self, board, white_to_play=True):
        self.board = board
        self.white_to_play = white_to_play
        self.moves = []
        self.view = BoardView(self.board)
        
    def move(self, move):
        # update logic here
        done = False
        if not done:
            done = self._pawn_move(move)
        if not done:
            done = self._knight_move(move)
        if not done:
            done = self._bishop_move(move)
        if not done:
            done = self._rook_move(move)
        if not done:
            done = self._queen_move(move)
        if not done:
            done = self._king_move(move)
        
        self.white_to_play = not self.white_to_play

    def _pawn_move(self, move):
        if self.white_to_play:
            return self._white_pawn_move(move)
        else:
            return self._black_pawn_move(move)

    def _knight_move(self, move):
        return False

    def _bishop_move(self, move):
        return False

    def _rook_move(self, move):
        return False

    def _queen_move(self, move):
        return False

    def _king_move(self, move):
        return False 

    def _white_pawn_move(self, move):
        if len(move) == 2:
            if self.board[move] != ' ':
                return False
            rank = int(move[-1])
            done = self._move_white_pawn_one_rank(move, rank)
            if not(done) and rank == 4:
                done = self._move_white_pawn_two_ranks(move, rank)            
            return done
        else:
            return False

    def _move_white_pawn_two_ranks(self, move, rank):
        if self.board[move.replace(str(rank), str(rank - 2))] != 'w' \
                or self.board[move.replace(str(rank), str(rank - 1))] != ' ' \
                or rank != 4:
            return False
        
        pawn_position = move.replace(str(rank), str(rank - 2))
        return self._update_board(move, pawn_position, move)

    def _move_white_pawn_one_rank(self, move, rank):
        if self.board[move.replace(str(rank), str(rank - 1))] != 'w':
            return False

        pawn_position = move.replace(str(rank), str(rank - 1))
        return self._update_board(move, pawn_position, move)
        
    def _update_board(self, move, old, new):
        self.board[new] = self.board[old]
        self.board[old] = ' '
        self.moves.append(move)
        return True
    
    def _black_pawn_move(self, move):
        return False

    def __str__(self):
        self.view.isFlipped = not self.white_to_play
        return str(self.view)

def main(*args, **kwargs):
    board = BOARD_FACTORY.build('EMPTY')
    board['a2'] = 'w'
    chess = ChessEngine(board)
    print(chess)
    chess.move('a3')
    print(BoardView(board))

if __name__ == "__main__":
    main()