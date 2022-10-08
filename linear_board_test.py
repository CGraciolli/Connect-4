import pytest
from linear_board import LinearBoard
from settings import BOARD_SIZE, VICTORY_STRIKE

def test_empty_board():
    empty = LinearBoard()
    assert empty != None
    assert empty.is_full() == False
    assert empty.is_victory('x') == False

def test_add():
    b = LinearBoard()
    for _ in range(BOARD_SIZE):
        b.add('x')
    assert b.is_full() == True

def test_victory():
    b = LinearBoard()
    for i in range(VICTORY_STRIKE):
        b.add('x')
    assert b.is_victory('o') == False
    assert b.is_victory('x') == True
    
def test_tie():
    b = LinearBoard()
    b.add('x')
    b.add('x')
    b.add('o')
    b.add('x')
    b.add("o")
    assert b.is_tie("x", "o") == True

def test_add_to_full():
    b = LinearBoard()
    for i in range(BOARD_SIZE + 1):
        b.add('x')
    assert len(b.column) == BOARD_SIZE

def test_from_list():
    b = LinearBoard.from_list(["x", "o", None, None, None])
    c = LinearBoard()
    c.add("x")
    c.add("o")

    assert b == c

def test_is_victory():
    L = LinearBoard.from_list(["x", "o", "o", "o", "o"])

    assert L.is_victory("o") == True
    assert L.is_victory("x") == False

