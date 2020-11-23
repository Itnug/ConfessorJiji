
import re

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

GAME = None

def discord_view(board):
    view = '\n'
    br = '+'+'----+'*8
    view += br + '\n'
    for j in RANKS[::-1]:
        line = '|'
        offset = 0
        for i in FILES:
            position = i + j
            if offset >= 1:
                padding = ' '
                offset -= 1
            else:
                padding = ''

            if board[position]:
                offset += 0.34
                sprite = ' ' + board[position] + ' ' + padding
            else:
                sprite = '    ' + padding
            line += sprite + '|'
        view += line + '\n'
        view += br + '\n'
    return '```' + view + '```'

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

def get_user_from_mention(mention: str):
    if not mention: return
    if mention.startswith('<@') and mention.endswith('>'):
        mention = mention[2:-1]
        if mention.startswith('!'):
            mention = mention[1:]

@bot.command(name='e')
async def test(ctx):
    print(ctx.__dir__())

@bot.event
async def on_ready():
    print(f'chessbot is online')

@bot.command(name='chess')
async def chess(ctx, opponent):
    global GAME
    if GAME:
        await ctx.send('I can only run one game. use `!abort` or wait till the game is over')
        return
    white = str(ctx.author.id)
    black = re.sub('[<@!>]', '', opponent) 
    GAME = Chess(white=white, black=black)

    await ctx.send(f"<@{white}>(white) vs <@{black}>(black).")

@bot.command(name='abort')
async def abort(ctx):
    global GAME
    GAME = None

@bot.command(name='move')
async def move(ctx, move):
    global GAME
    print(f'to play = {GAME.get_current_player()}')
    player = str(ctx.author.id)
    if GAME.is_valid_player(player):
        if GAME.is_valid_move(move):
            await ctx.send(f'ok <@{player}>.')
            GAME.toggle_player()
        else:
            await ctx.send(f'that is an illegal move. bruh...')
        await ctx.send(f'now it is <@{GAME.get_current_player()}>\'s turn')
    else:
        await ctx.send(f'invalid player. <@{ctx.author.id}> not same as <@{GAME.get_current_player()}>')

@bot.command(name='whoseturn')
async def whose_turn(ctx):
    global GAME
    await ctx.send(f'<@{GAME.get_current_player()}>')

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