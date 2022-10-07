import pytest
from list_tools import transpose_matrix
from square_board import SquareBoard

def test_empty_board():
    board = SquareBoard()

    assert board.is_full() == False
    assert board.is_victory('x') == False
    assert board.is_victory('o') == False

def test_add():
    b = SquareBoard.from_list([["x", "o", "x", "o"], 
                                [None, None, None, None],
                                ["x", "o", None, None],
                                ["x", "x", "o", None]])
    c = SquareBoard.from_list([["x", "o", "x", "o"], 
                                [None, None, None, None],
                                ["x", "o", None, None],
                                ["x", "x", "o", None]])
    d = SquareBoard.from_list([["x", "o", "x", "o"], 
                                [None, None, None, None],
                                ["x", "o", None, None],
                                ["x", "x", "o", None]])
    
    b.add(0, "x")
    d.add(1, "o")
    c.add(2, "x")
    assert b == SquareBoard.from_list([["x", "o", "x", "o"], 
                                        [None, None, None, None],
                                        ["x", "o", None, None],
                                        ["x", "x", "o", None]]) 
    assert d == SquareBoard.from_list([["x", "o", "x", "o"], 
                                                   ["o", None, None, None],
                                                   ["x", "o", None, None],
                                                   ["x", "x", "o", None]])
    
    assert c == SquareBoard.from_list([["x", "o", "x", "o"], 
                                                   [None, None, None, None],
                                                   ["x", "o", "x", None],
                                                   ["x", "x", "o", None]])

def test_victory_vertical():
    vertical = SquareBoard.from_list([['x', 'o', 'o', 'o'], 
                                      [None, None, None, None], 
                                      [None, None, None, None], 
                                      [None, None, None, None]])

    assert vertical._vertical_victory('o') == True
    assert vertical._vertical_victory('x') == False

def test_horizontal_victory():
    a = SquareBoard.from_list([["x", "o", "x", "o"], 
                                ["x", None, None, None],
                                ["x", "o", None, None],
                                ["o", "x", "o", None]])
    b = SquareBoard.from_list([["x", "o", "x", "o"], 
                                [None, None, None, None],
                                ["x", "o", None, None],
                                ["x", "x", "o", None]])
    
    assert a._horizontal_victory("x") == True
    assert a._horizontal_victory("o") == False
    assert b._horizontal_victory("o") == False
    assert b._horizontal_victory("x") == False

def test_diag_desc_victory():
    diagonal = SquareBoard.from_list([['x', 'o', 'o', 'x'], 
                                     ['o', 'o', 'x', None], 
                                     ['x', 'x', None, None], 
                                     [None, None, None, None]])
    
    diagonal2 = SquareBoard.from_list([[None, 'o', 'o', 'x'],
                                       [None, 'o', 'x', 'o'],
                                       ['o', None, None, 'x'],
                                       [None, None, None, None]])
    
    diagonal4 = SquareBoard.from_list([[None, None, 'o', 'x'],
                                      [None, 'o', 'x', 'o'],
                                      ['o', 'o', 'x', 'x'],
                                      [None, None, None, None]])

    assert diagonal._descending_victory('o') == False
    assert diagonal._descending_victory('x') == True
    assert diagonal2._descending_victory('o') == True
    assert diagonal2._descending_victory('x') == False
    assert diagonal4._descending_victory('x') == False
    assert diagonal4._descending_victory('o') == True

def test_diag_asc_victoryy():
    diagonal = SquareBoard.from_list([['x', 'o', None, None], 
                                     ['o', 'x', 'o', None], 
                                     ['x', 'x', 'o', 'o'], 
                                     [None, None, None, None]])
    
    diagonal2 = SquareBoard.from_list([['x', 'o', None, None],
                                      ['o', 'x', None, None],
                                      ['x', 'o', 'x', 'o'],
                                      ['x', 'o', None, None]])

    assert diagonal._rising_victory('x') == False
    assert diagonal._rising_victory('o') == True
    assert diagonal2._rising_victory('x') == True
    assert diagonal2._rising_victory('o') == False

def test_is_winning_move():
    b = SquareBoard.from_list([["x", "x", None, None],
                                ["o", None, None, None],
                                [None, None, None, None],
                                [None, None, None, None]])
    c = SquareBoard.from_raw_code("x...|oo..|o...|....")

    assert b.is_winning_move(0, "x") == True
    assert b.is_winning_move(0, "o") == False
    assert b.is_winning_move(1, "x") == False
    assert b ==  SquareBoard.from_list([["x", "x", None, None],
                                ["o", None, None, None],
                                [None, None, None, None],
                                [None, None, None, None]])
    assert c.is_winning_move(1, "o")

def test_is_losing_move():
    b = SquareBoard.from_list([["x", "x", None, None],
                                ["o", None, None, None],
                                [None, None, None, None],
                                [None, None, None, None]])
    
    assert b.is_losing_move(0, "o") == False
    assert b.is_losing_move(1, "o") == True
    assert b.is_losing_move(2, "o") == True
    assert b.is_losing_move(3, "o") == True
    assert b.is_losing_move(2, "x") == False
    assert b == SquareBoard.from_list([["x", "x", None, None],
                                ["o", None, None, None],
                                [None, None, None, None],
                                [None, None, None, None]])

def test_board_code():
    b = SquareBoard.from_list([["x", "x", None, None],
                                ["o", None, None, None],
                                [None, None, None, None],
                                [None, None, None, None]])
    code = b.as_code()
    clone_board = SquareBoard.from_code(code)

    assert clone_board == b
    assert clone_board.as_code() == code
    assert clone_board.as_code()._raw_code == code._raw_code