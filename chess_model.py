from collections import namedtuple

Sprite = namedtuple('Sprite', ('name', 'id',  'view'))
sprites = [
    Sprite('white_king', 11, '♔'),
    Sprite('white_queen', 12, '♕'),
    Sprite('white_rook', 13, '♖'),
    Sprite('white_bishop', 14, '♗'),
    Sprite('white_knight', 15, '♘'),
    Sprite('white_pawn', 16, '♙'),

    Sprite('black_king', 21, '♚'),
    Sprite('black_queen', 22, '♛'),
    Sprite('black_rook', 23, '♜'),
    Sprite('black_bishop', 24, '♝'),
    Sprite('black_knight', 25, '♞'),
    Sprite('black_pawn', 26, '♟︎'),

    Sprite('h_break', 101, '〰'),
    Sprite('empty_space', 102, '　') #unicode space - extra wide
]

sprites_memo = {}
def sprite_by_id(id):
    if id in sprites_memo:
        return sprites_memo[id]

    for sprite in sprites:
        if sprite.id == id:
            sprites_memo[id] = sprite
            return sprite
    
    raise ValueError('no sprite exists for id = ' + str(id))

def sprite_by_name(name):
    if id in sprites_memo:
        return sprites_memo[name]

    for sprite in sprites:
        if sprite.name == name:
            sprites_memo[name] = sprite
            return sprite
    
    raise ValueError('no sprite exists for name = ' + name)

v_break = '|'
hv_intersection = '.'


class Board():
    
    def __init__(self, iterable=None):
        if not iterable:
            iterable = map(lambda x: x.id, [sprite_by_name('empty_space')]*64) 
        
        self.model = list(iterable)
        if len(self.model) != 64:
            raise ValueError(f"chess boards have 64 squares genius. {len(self.model)} != 64")

    def __setitem__(self, key, newValue):
        if isinstance(key, str):
            _index = Board.toIndex(key)
            self.model[_index] = newValue

    def __getitem__(self, key):
        if isinstance(key, str):
            _index = Board.toIndex(key)
            return self.model[_index]

        return self.model.__getitem__(key)

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
        h_break = sprite_by_name('h_break')
        empty_space = sprite_by_name('empty_space')
        break_line = '  ' + '+'.join(['']+[f' {h_break.view} '] * 8 +['']) + '\n'
        view_ranks = []
        
        rank_range = self._flip(range(8))
        file_range = self._flip('ABCDEFGH') 
        
        for i in rank_range:
            spot_range = self._flip(self.board[(7-i)*8:(7-i)*8+8])
            rank_items = map(lambda x: f' {sprite_by_id(x).view} ', spot_range)
            view_ranks.append(f'{str(8-i)} ' + '|'.join(['',*rank_items,'']) + '\n')

        view = break_line.join(['', *view_ranks, ''])
        view += f'   {empty_space.view}' + f'{empty_space.view}  '.join(file_range)
        return view

class BoardFactory():
    
    def __init(self):
        pass
    
    def build(self, spec):
        if not spec:
            return self.full()

        if spec.upper() == 'EMPTY':
            return Board()
        else:
            return self.full()

    def full(self):
        board = Board([
            sprite_by_name('white_rook').id,
            sprite_by_name('white_knight').id,
            sprite_by_name('white_bishop').id,
            sprite_by_name('white_queen').id,
            sprite_by_name('white_king').id,
            sprite_by_name('white_bishop').id,
            sprite_by_name('white_knight').id,
            sprite_by_name('white_rook').id,

            *map(lambda x: x.id, [sprite_by_name('white_pawn')]*8),
            *map(lambda x: x.id, [sprite_by_name('empty_space')]*32),
            *map(lambda x: x.id, [sprite_by_name('black_pawn')]*8),
            
            sprite_by_name('black_rook').id,
            sprite_by_name('black_knight').id,
            sprite_by_name('black_bishop').id,
            sprite_by_name('black_queen').id,
            sprite_by_name('black_king').id,
            sprite_by_name('black_bishop').id,
            sprite_by_name('black_knight').id,
            sprite_by_name('black_rook').id
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
         
class Chess():

    def __init__(self, whitePlayer, blackPlayer):
        self.players = {
            'white': whitePlayer,
            'black': blackPlayer 
        }
        self.moves = []
        self._current = 'white'

    def update(self, player, move):
        if self.current_player() != player:
            return InvalidPlayer
        move = Move(move)

        self.toggle_player()

    def current_player(self):
        return self.players[self._current]

    def toggle_player(self):
        if self._current == 'white':
            self._current = 'black'
        else:
            self._current = 'white'
    

def main(*args, **kwargs):
    board = BOARD_FACTORY.build('FULL')
    board['e4'] = sprite_by_name('black_pawn').id
    print(board['e4'])
    print(BoardView(board))

if __name__ == "__main__":
    main()