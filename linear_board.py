from types import ClassMethodDescriptorType
from settings import BOARD_SIZE, VICTORY_STRIKE
from list_tools import find_n_cons

class LinearBoard:
    """
    represents a board with a single column
    x for player 1, o for player 2, None for empty space
    """

    @classmethod
    def fromList(cls, list):
        board = cls()
        board.column = list
        return list
        
    def __init__(self):
        """
        creates an empty linear board
        """
        self.column = [None] * BOARD_SIZE
        self.board_length = BOARD_SIZE
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.column == other.column
        return False
    
    def __len__(self):
        return len(self.column)
    
    def __getitem__(self, key):
        return self.column[key]
    
    def __repr__(self):
        return f'Linear Board: {self.column}'


    @classmethod
    def from_list(cls, lista):
        if len(lista) != BOARD_SIZE:
            raise Exception("Wrong dimensions")
        ##creates a empty board?    
        board = cls()
        board.column = lista
        return board
    
    def add(self, char):
        """
        adds a piece from player
        """
        if not self.is_full():
            place = self.column.index(None)
            self.column[place] = char
    
    def is_victory(self, char):
        return find_n_cons(self.column, char, VICTORY_STRIKE)

    def is_full(self):
        return self.column[-1] != None

    def is_tie(self, char1, char2):
        if self.is_full():
            if not self.is_victory(char1) and not self.is_victory(char2):
                return True
        return False
