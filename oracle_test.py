import pytest
from oracle import *
from square_board import SquareBoard, BoardCode
from player import Player
from move import Move

def test_base_oracle():
    board = SquareBoard.from_raw_code("xoxox|.....|.....|.....|x....") 
    expected = [ColumnRecommendation(0, ColumnClassification.FULL),
                ColumnRecommendation(1, ColumnClassification.MAYBE),
                ColumnRecommendation(2, ColumnClassification.MAYBE),
                ColumnRecommendation(3, ColumnClassification.MAYBE),
                ColumnRecommendation(3, ColumnClassification.MAYBE)
                ]
    oracle = BaseOracle()

    assert len(oracle.get_recommendation(board, None)) == len(expected)
    assert oracle.get_recommendation(board, None) == expected

def test_update_to_bad():
    board = SquareBoard()
    board_code = BoardCode(board)
    o = LearningOracle()
    jaco = Player("Jaco", "x", oracle=o)
    m = Move(0, board_code, None, jaco)
    o.update_to_bad(m)

    assert o.get_recommendation(board, jaco.char)[0] == ColumnRecommendation(0, ColumnClassification.BAD)

def test_no_good_options():
    j = Player("Jaco", "x")
    l = Player("Lua", "o", opponent=j)
    j.opponent = l

    oracle = SmartOracle()

    maybe = SquareBoard.from_raw_code(".....|o....|.....|.....|.....")
    bad_and_full = SquareBoard.from_raw_code("xoxxx|ooo..|oo...|ox...|.....")
    all_bad = SquareBoard.from_raw_code("x....|ooo..|oox..|ox...|.....")

    assert oracle.no_good_options(maybe, j) == False
    assert oracle.no_good_options(bad_and_full, j) == True
    assert oracle.no_good_options(all_bad, j) == True