import unittest
from chess_model import sprite_by_name, BOARD_FACTORY, ChessEngine

def board_view(board):
    view = '\n'
    br = '+'+'---+'*8
    view += br + '\n'
    for j in '87654321':
        line = '|'
        for i in 'abcdefgh':
            position = i + j
            if board[position] != ' ':
                sprite = sprite_by_name(board[position]).view
            else:
                sprite = ' '
            line += ' ' + sprite + ' |'
        view += line + '\n'
        view += br + '\n'
    return view

class TestChessModel(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_board(self):
        board = BOARD_FACTORY.build("FULL")
        print(board_view(board))
        assert board['a1'] == 'wR'
        assert board['e4'] == ' '
        assert board['e8'] == 'bK'    

    def test_equate_boards(self):
        board1 = BOARD_FACTORY.build("FULL")
        board2 = BOARD_FACTORY.build("FULL")
        assert board1 == board2

    def test_white_pawn_moves_one_step(self):
        board = BOARD_FACTORY.build("EMPTY")
        board['e2'] = 'w'
        chess = ChessEngine(board)
    
        expected_board = BOARD_FACTORY.build("EMPTY")
        expected_board['e3'] = 'white_pawn'
    
        chess.move('e3')
        assert expected_board == board
    
    def test_white_pawn_moves_two_steps(self):
        board = BOARD_FACTORY.build("EMPTY")
        board['e2'] = 'w'
        chess = ChessEngine(board)
    
        expected_board = BOARD_FACTORY.build("EMPTY")
        expected_board['e4'] = 'white_pawn'
    
        chess.move('e4')
        assert expected_board == board
    
    def test_white_pawn_doesnt_moves_two_steps_when_not_in_rank_2(self):
        board = BOARD_FACTORY.build("EMPTY")
        board['e3'] = 'w'
        chess = ChessEngine(board)
    
        chess.move('e5')
        
        assert board['e3'] == 'w'


if __name__ == "__main__":
    unittest.main()