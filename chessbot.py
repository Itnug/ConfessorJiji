import re

from discord.ext import commands
from chess_model import BoardView, BOARD_FACTORY, sprite_by_name

bot = commands.Bot(command_prefix='!')

_piece = '[KQBNR]'
_check = '[+#]'
_rank = '[1-8]'
_file = '[a-h]'

_promotion = f'x?{_file}[18]=(?!K){_piece}'
_pawnmove = f'(?:{_file}?x)?{_file}(?![18]){_rank}'
_stdmove   = f'{_piece}{_file}?{_rank}?x?{_file}{_rank}'
_castling  = 'O-O(?:-O)?'

_notation = f'({_promotion}|{_castling}|{_pawnmove}|{_stdmove}){_check}?'
notation = re.compile(_notation)

#global variables
CACHE = {}

def get_user_from_mention(mention: str):
    if not mention: return
    if mention.startswith('<@') and mention.endswith('>'):
        mention = mention[2:-1]
        if mention.startswith('!'):
            mention = mention[1:]

@bot.event
async def on_ready():
    print(f'chessbot is online')

@bot.command(name='chess')
async def chess(ctx, opponent):
    global CACHE
    if CACHE['GAME']:
        await ctx.send('I can only run one game. use `!abort` or wait till the game is over')
        return
    white = str(ctx.author.id)
    black = re.sub('[<@!>]', '', opponent) 
    CACHE['GAME'] = Chess(white=white, black=black)

    await ctx.send(f"<@{white}>(white) vs <@{black}>(black).")

@bot.command(name='abort')
async def abort(ctx):
    global CACHE
    CACHE['GAME'] = None

@bot.command(name='move')
async def move(ctx, move):
    global CACHE
    game = CACHE['GAME']
    print(f'to play = {game.get_current_player()}')
    player = str(ctx.author.id)
    if game.is_valid_player(player):
        if game.is_valid_move(move):
            await ctx.send(f'ok <@{player}>.')
            game.toggle_player()
        else:
            await ctx.send(f'that is an illegal move. bruh...')
        await ctx.send(f'now it is <@{game.get_current_player()}>\'s turn')
    else:
        await ctx.send(f'invalid player. <@{ctx.author.id}> not same as <@{game.get_current_player()}>')

@bot.command(name='whoseturn')
async def whose_turn(ctx):
    global CACHE
    player = CACHE['GAME'].get_current_player()
    await ctx.send(f'<@{player}>')

async def create_board(ctx, init='FULL', name='DEFAULT'):
    if name.lower() in ('active', 'create'):
         await ctx.send(f'board name {name} is prohibited')
         return

    global CACHE
    boards = CACHE.setdefault('BOARDS',{})
    reply = ''

    if name not in boards:
        boards[name] = BOARD_FACTORY.build(init)
    board = boards[name]
    CACHE['ACTIVE_BOARD'] = name
    reply += view_board(name, board)
    await ctx.send(reply)

@bot.command(name='placePieces')
async def placePieces(ctx, placements):
    global CACHE
    name = CACHE.setdefault('ACTIVE_BOARD', 'DEFAULT')
    boards = CACHE.setdefault('BOARDS',{})
    if name not in boards:
        boards[name] = BOARD_FACTORY.build('FULL') 
    
    board = boards[name]
    reply = ''
    for placement in placements.split(','):
        place, piece = placement.split('=')
        board[place] = piece
    
    reply += view_board(name, board)
    await ctx.send(reply)

def view_board(name, board):
    view = BoardView(board)
    return f'board[{name}]:\n```{view}```'

@bot.command(name='board')
async def board(ctx, *args):
    global CACHE
    boards = CACHE.setdefault('BOARDS',{})
    if not args:
        await ctx.send(f'boards list(in memory): {list(boards.keys())}')
        return
    if args[0].lower() == 'create':
        await create_board(ctx, *args[1:])
        return

    name = args[0]
    if name.upper() == 'ACTIVE':
        name = CACHE['ACTIVE_BOARD']
    if name in boards:
        CACHE['ACTIVE_BOARD'] = name
        board = boards[name]
        reply = view_board(name, board)
        await ctx.send(reply)
    else:
        await ctx.send(f'no board with name {name}')

class Chess():

    def __init__(self, *args, **kwargs):
        self.white = kwargs['white']
        self.black = kwargs['black'] 
        print(f'white = {self.white}')
        print(f'black = {self.black}')
        self.to_play = 0
    
    def toggle_player(self):
        self.to_play += 1
        self.to_play %= 2
    
    def is_valid_player(self, player):
        print(str(player))
        print(self.get_current_player())

        return str(player) == self.get_current_player()

    def get_current_player(self):
        return self.black if self.to_play else self.white

    def is_valid_move(self, move):
        if re.match(notation, move):
            return True
        else:
            return False

if __name__ == "__main__":
    board = BOARD_FACTORY.build('FULL')
    print(view_board('DEFAULT', board))
