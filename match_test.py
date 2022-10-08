import pytest
from match import Match
from player import Player, HumanPlayer
from square_board import SquareBoard

def setup():
    global jaco
    jaco = Player("Jaco")
    global lua
    lua = HumanPlayer("Lua")

def teardown():
    global jaco
    jaco = None
    global lua
    lua = None

def test_dif_player_dif_char():
    m = Match(jaco, lua)

    assert jaco.char != lua.char

def test_no_player_with_None_char():
    m = Match(jaco, lua)

    assert jaco.char != None
    assert lua.char != None

def test_next_player_is_round_robbin():
    m = Match(jaco, lua)

    p1 = m.next_player ##next player isn´t followed by () because it is a property, not a function
    p2 = m.next_player
    p3 = m.next_player
    p4 = m.next_player

    assert p1 != p2
    assert p1 == p3
    assert p2 == p4

def test_players_are_opponents():
    m = Match(jaco, lua)

    p1 = m.next_player
    p2 = m.next_player

    assert p1.opponent == p2
    assert p2.opponent == p1

def test_get_winner():
    m = Match(jaco, lua)
    b1 = SquareBoard.from_raw_code("xo...|x....|xo...|xo...|.....")
    b2 = SquareBoard.from_raw_code("oooo.|x....|xo...|xo...|.....")
    b3 = SquareBoard.from_raw_code("xoxox|ooxox|oxooo|xoxxx|xoxxo") 
    
    assert m.get_winner(b1) == m.player1
    assert m.get_winner(b2) == m.player2
    assert m.get_winner(b3) == None
