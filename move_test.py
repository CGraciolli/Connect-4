from move import Move
import pytest
from square_board import BoardCode, SquareBoard
from oracle import LearningOracle
from player import ReportingPlayer
from settings import BOARD_SIZE

def test_symmetric_move():
    b = BoardCode.from_raw_code("xxx..|o....|o....|ox...|.....")
    sb = BoardCode.from_raw_code(".....|ox...|o....|o....|xxx..")
    j = ReportingPlayer("Jaco", "x", oracle = LearningOracle())
    rec_b = j.oracle.get_recommendation(SquareBoard.from_code(b), j.char)
    rec_sb = j.oracle.get_recommendation(SquareBoard.from_code(sb), j.char)

    for i in range(BOARD_SIZE):
        assert b.symmetric() == sb
        assert Move(i, b, rec_b, j).symmetric_move() == Move(BOARD_SIZE - 1 -i, sb, rec_sb, j)