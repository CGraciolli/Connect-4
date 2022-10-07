import pytest
from game import Game
from square_board import SquareBoard


def test_creation():
    g = Game()
    
    assert g != None

def test_is_game_over():
    empty = Game()
    g1 = Game()
    g1.board = SquareBoard.from_list([["x", "o", None, None],
                                      ["o", None, None, None],
                                      ["o", None, None, None],
                                      ["x", None, None, None]])
    g2 = Game()
    g2.board = SquareBoard.from_list([["x", "o", None, None],
                                      ["o", None, None, None],
                                      ["o", None, None, None],
                                      ["o", None, None, None]])
    g3 = Game()
    g3.board= SquareBoard.from_list([["o", "x", "x", "o"],
                                 ["x", "o", "o", "x"],
                                 ["o", "x", "x", "o"],
                                 ["x", "o", "o", "x"]])    

    g4 = Game()
    g4.board = SquareBoard.from_list([["x", "x", "x", None],
                                      ["o", None, None, None],
                                      ["o", None, None, None],
                                      ["x", None, None, None]])                         

    assert empty.has_winner_or_is_a_tie() == False
    assert g1.has_winner_or_is_a_tie() == False
    assert g2.has_winner_or_is_a_tie() == True
    assert g3.has_winner_or_is_a_tie() == True
    assert g4.has_winner_or_is_a_tie() == True



    