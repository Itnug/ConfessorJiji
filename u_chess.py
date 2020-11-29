from chess_model import BoardView, BOARD_FACTORY, sprite_by_name

def white_pawn_move(board, move):
    if len(move) == 2:
        if board[move] != ' ':
            return 'illegal move'
        rank = int(move[1])
        file = move[0]
        if rank == 4:
            if board[move.replace(str(rank), str(rank - 1))] == 'w':
                pawn_position = move.replace(str(rank), str(rank - 1))
                return 'pawn moved to ' + move + ' from ' + pawn_position
            elif board[move.replace(str(rank), str(rank - 2))] == 'w' and board[move.replace(str(rank), str(rank - 1))] == ' ':
                pawn_position = move.replace(str(rank), str(rank - 2))
                return 'pawn moved to ' + move + ' from ' + pawn_position
            else:
                return 'illegal move'
        else:
            if board[move.replace(str(rank), str(rank - 1))] == 'w':
                pawn_position = move.replace(str(rank), str(rank - 1))
                return 'pawn moved to ' + move + ' from ' + pawn_position

if __name__ == "__main__":
    board = BOARD_FACTORY.build('FULL')
    print(white_pawn_move(board, 'e3'))