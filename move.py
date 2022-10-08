
from settings import BOARD_SIZE

class Move:

    def __init__(self, position, board_code, rec, player):
        self.position = position
        self.board_code = board_code
        self.rec = rec
        self.player = player
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.position == other.position and self.board_code == other.board_code and self.rec == other.rec and self.player.char == other.player.char:
                return True
            return False
        return False
    def __hash__(self):
        return hash(self.position, self.board_code, self.rec, self.player)

    def symmetric_move(self):
        """
        is given a move and returns another move,
        using that the board is symmetric
        """
        new_position = BOARD_SIZE -1 -self.position
        new_board_code = self.board_code.symmetric()
        new_rec = self.rec[::-1]
        return Move(new_position, new_board_code, new_rec, self.player)