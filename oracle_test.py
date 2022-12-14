import pytest
from oracle import *
from square_board import SquareBoard, BoardCode
from player import Player
from move import Move
from settings import BOARD_SIZE

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

def test_get_recommendation():
    o = MemoizingOracle()
    code = BoardCode.from_raw_code(".....|ooo..|.....|.....|xxx..")
    swapped_code = BoardCode.from_raw_code(".....|xxx..|.....|.....|ooo..")
    swap_sym_code = swapped_code.symmetric()
    key = o.make_key(code, "x")
    board = SquareBoard.from_code(code)
    rec = o.get_recommendation(board, "x")
    o.knowledge.past_rec = {key : rec}

    symcode = code.symmetric()

    o.get_recommendation(SquareBoard.from_code(symcode), "x")

    assert len(o.knowledge) == 1
    for i in range(BOARD_SIZE):
        o.get_recommendation(SquareBoard.from_code(symcode), "x")[i] == rec[BOARD_SIZE -1 -i]
        o.get_recommendation(SquareBoard.from_code(code), "x")[i] == o.get_recommendation(SquareBoard.from_code(swapped_code), "o")[i]
        o.get_recommendation(SquareBoard.from_code(swap_sym_code), "o")[i] == rec[BOARD_SIZE -1 -i]
    
def test_is_winning_move():
    b = SquareBoard.from_raw_code(".....|xo...|xo...|x....|.....")
    c = SquareBoard.from_raw_code("x....|ooo..|o....|x....|.....")
    o = SmartOracle()
    assert o.is_winning_move(b, 0, "x") == True
    assert o.is_winning_move(b, 0, "o") == False
    assert o.is_winning_move(b, 1, "x") == False
    assert b == SquareBoard.from_raw_code(".....|xo...|xo...|x....|.....")
    assert o.is_winning_move(c, 1, "o")

def test_is_losing_move():
    b = SquareBoard.from_raw_code("xxx..|xo...|ooo..|x....|.....")
    o = SmartOracle()

    assert o.is_losing_move(b, 0, "o") == False
    assert o.is_losing_move(b, 1, "o") == True
    assert o.is_losing_move(b, 2, "o") == True
    assert o.is_losing_move(b, 3, "o") == True
    assert o.is_losing_move(b, 4, "o") == True
    assert o.is_losing_move(b, 2, "x") == False
    assert b == SquareBoard.from_raw_code("xxx..|xo...|ooo..|x....|.....")