import pytest
from game import Game, get_base_knowledge
from square_board import SquareBoard
from player import ReportingPlayer
from oracle import LearningOracle


def test_creation():
    g = Game()
    
    assert g != None

def test_is_game_over():
    empty = Game()
    g1 = Game()
    g1.board = SquareBoard.from_raw_code("xo...|o....|o....|x....|x....")
    g2 = Game()
    g2.board = SquareBoard.from_raw_code("xo...|o....|o....|o....|ox...")
    g3 = Game()
    g3.board= SquareBoard.from_raw_code("xoxox|ooxox|oxooo|xoxxx|xoxxo")  

    g4 = Game()
    g4.board = SquareBoard.from_raw_code("xxxx.|o....|o....|.....|ox...")                     

    assert empty.has_winner_or_is_a_tie() == False
    assert g1.has_winner_or_is_a_tie() == False
    assert g2.has_winner_or_is_a_tie() == True
    assert g3.has_winner_or_is_a_tie() == True
    assert g4.has_winner_or_is_a_tie() == True

def test_get_base_knowledge():
    p1 = ReportingPlayer("Jaco", oracle = LearningOracle())
    p2 = ReportingPlayer("Lua", oracle = LearningOracle())
    get_base_knowledge(20, p1, p2)

    assert p1.oracle.knowledge.past_rec != {}
    assert len(p1.oracle.knowledge) >= len(p2.oracle.knowledge)






    