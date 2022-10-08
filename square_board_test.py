import pytest
from square_board import SquareBoard

def test_empty_board():
    board = SquareBoard()

    assert board.is_full() == False
    assert board.is_victory('x') == False
    assert board.is_victory('o') == False

def test_add():
    b = SquareBoard.from_raw_code("xoxo.|.....|xo...|xxo..|.....")
    c = SquareBoard.from_raw_code("xoxo.|.....|xo...|xxo..|.....")
    d = SquareBoard.from_raw_code("xoxo.|.....|xo...|xxo..|.....")
    b.add(0, "x")
    d.add(1, "o")
    c.add(2, "x")
    assert b == SquareBoard.from_raw_code("xoxox|.....|xo...|xxo..|.....")
    assert d == SquareBoard.from_raw_code("xoxo.|o....|xo...|xxo..|.....")
    
    assert c == SquareBoard.from_raw_code("xoxo.|.....|xox..|xxo..|.....")

def test_victory_vertical():
    vertical = SquareBoard.from_raw_code("xoxo.|oooo.|xo...|xxo..|.....")

    assert vertical._vertical_victory('o') == True
    assert vertical._vertical_victory('x') == False

def test_horizontal_victory():
    a = SquareBoard.from_raw_code("xoxo.|x....|xo...|xxo..|.....")
    b = SquareBoard.from_raw_code("xoxo.|ox...|xo...|xoo..|.....")
    
    assert a._horizontal_victory("x") == True
    assert a._horizontal_victory("o") == False
    assert b._horizontal_victory("o") == False
    assert b._horizontal_victory("x") == False

def test_diag_desc_victory():
    diagonal = SquareBoard.from_raw_code("oxox.|oox..|ox...|x....|.....")
    
    diagonal2 = SquareBoard.from_raw_code("xxox.|xxxo.|oxo..|oo...|o....")
    
    assert diagonal._descending_victory('o') == False
    assert diagonal._descending_victory('x') == True
    assert diagonal2._descending_victory('o') == True
    assert diagonal2._descending_victory('x') == False

def test_diag_asc_victoryy():
    diagonal = SquareBoard.from_raw_code("xo...|xxo..|oxxo.|xxooo|.....")
    
    
    diagonal2 = SquareBoard.from_raw_code(".....|x....|ox...|oox..|oxxx.")
    

    assert diagonal._rising_victory('x') == False
    assert diagonal._rising_victory('o') == True
    assert diagonal2._rising_victory('x') == True
    assert diagonal2._rising_victory('o') == False

def test_is_winning_move():
    b = SquareBoard.from_raw_code(".....|xo...|xo...|x....|.....")
    c = SquareBoard.from_raw_code("x....|ooo..|o....|x....|.....")

    assert b.is_winning_move(0, "x") == True
    assert b.is_winning_move(0, "o") == False
    assert b.is_winning_move(1, "x") == False
    assert b == SquareBoard.from_raw_code(".....|xo...|xo...|x....|.....")
    assert c.is_winning_move(1, "o")

def test_is_losing_move():
    b = SquareBoard.from_raw_code("xxx..|xo...|ooo..|x....|.....")
    
    assert b.is_losing_move(0, "o") == False
    assert b.is_losing_move(1, "o") == True
    assert b.is_losing_move(2, "o") == True
    assert b.is_losing_move(3, "o") == True
    assert b.is_losing_move(4, "o") == True
    assert b.is_losing_move(2, "x") == False
    assert b == SquareBoard.from_raw_code("xxx..|xo...|ooo..|x....|.....")

def test_board_code():
    b = SquareBoard.from_raw_code(".....|xo...|xo...|x....|.....")
    code = b.as_code()
    clone_board = SquareBoard.from_code(code)

    assert clone_board == b
    assert clone_board.as_code() == code
    assert clone_board.as_code()._raw_code == code._raw_code