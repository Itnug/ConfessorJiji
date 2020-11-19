from jiji_module import JijiModule
from games.chess import new_game, RANKS, FILES

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

class Chess(JijiModule):


    def on_message(self, message):
        token = message.content.lower().split()
        
        if token[0] != 'jiji':
            return
        
        if token[1] != 'chess':
            return
        
        board = new_game()
        return discord_view(board)
    
if __name__ == '__main__':
    test_string = 'jiji  yin'
    print(test_string.split())