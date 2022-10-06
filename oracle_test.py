import pytest
from oracle import *
from square_board import SquareBoard, BoardCode
from player import Player
from list_tools import explode_to_matrix

def test_base_oracle():
    board = SquareBoard.from_list([["x", "o", "o", "x"],
                                   [None, None, None, None],
                                   [None, None, None, None],
                                   ["o", None, None, None]])
    expected = [ColumnRecommendation(0, ColumnClassification.FULL),
                ColumnRecommendation(1, ColumnClassification.MAYBE),
                ColumnRecommendation(2, ColumnClassification.MAYBE),
                ColumnRecommendation(3, ColumnClassification.MAYBE)]
    oracle = BaseOracle()

    assert len(oracle.get_recommendation(board, None)) == len(expected)
    assert oracle.get_recommendation(board, None) == expected

def test_update_to_bad():
    board = SquareBoard()
    board_code = BoardCode(board)
    o = LearningOracle()
    jaco = Player("Jaco", "x", oracle=o)
    o.update_to_bad(board_code, jaco, 0)

    assert o.get_recommendation(board, jaco.char)[0] == ColumnRecommendation(0, ColumnClassification.BAD)

def test_no_good_options():
    j = Player("Jaco", "x")
    l = Player("Lua", "o", opponent=j)
    j.opponent = l

    oracle = SmartOracle()

    maybe = SquareBoard.from_raw_code("....|o...|....|....")
    bad_and_full = SquareBoard.from_raw_code("x...|oo..|o...|xoxo")
    all_bad = SquareBoard.from_raw_code("x...|oo..|o...|....")

    assert oracle.no_good_options(maybe, j) == False
    assert oracle.no_good_options(bad_and_full, j) == True
    assert oracle.no_good_options(all_bad, j) == True