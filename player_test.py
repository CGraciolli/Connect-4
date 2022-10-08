import pytest
from player import *
from square_board import SquareBoard


def test_is_int():
    assert is_int("4") == True
    assert is_int(" 4") == True
    assert is_int("4 ") == True
    assert is_int("-4") == True
    assert is_int("0") == True
    assert is_int("4.5") == False
    assert is_int("a") == False
    assert is_int("") == False

def test_is_within_range():
    b = SquareBoard()
    assert is_within_range(b, 0) == True
    assert is_within_range(b, 1) == True
    assert is_within_range(b, 2) == True
    assert is_within_range(b, 3) == True
    assert is_within_range(b, 5) == False
    assert is_within_range(b, -1) == False

def test_is_column_not_full():
    b = SquareBoard.from_raw_code("xoxox|x....|.....|.....|oo...")
    
    assert is_column_not_full(b, 0) == False
    assert is_column_not_full(b, 1) == True
    assert is_column_not_full(b, 2) == True
    assert is_column_not_full(b, 3) == True
    assert is_column_not_full(b, 4) == True