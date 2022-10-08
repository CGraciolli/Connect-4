from linear_board import LinearBoard
from settings import BOARD_SIZE
from list_tools import transpose_matrix, rot_matrix_ccw, invert_matrix, collapse_matrix, explode_to_matrix

class SquareBoard:
    """
    represents a square board
    x for player 1, o for player 2, None for empty space
    """
    def __init__(self):
        self.board_length = BOARD_SIZE
        self.columns = [LinearBoard() for i in range(BOARD_SIZE)]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.columns == other.columns
        return False
    
    def __hash__(self) -> int:
        return hash(self.columns)

    def __repr__(self):
        lines = []
        for i in range(len(self.columns[0]) - 1, -1, -1):
            line = "|"
            for column in self.columns:
                if column[i]:
                    line += column[i] + "|"
                else:
                    line += " |"
            line += "\n"
            lines.append(line)
        board = ""
        for line in lines:
            board += line
        return board

    @classmethod
    def from_list(cls, list_of_lists):
        """
        recieves a list of lists, returns a list of linear boards
        """
        if len(list_of_lists) != BOARD_SIZE:
            raise Exception("Wrong Dimensions")
        board = cls()
        board.columns = list(map(lambda element: LinearBoard.from_list(element), list_of_lists))
        return board
    
    @classmethod
    def from_code(cls, code):
        S = code.raw_code
        matrix = explode_to_matrix(S)
        b = cls.from_list(matrix)
        return b

    @classmethod
    def from_raw_code(cls, raw_code):
        matrix = explode_to_matrix(raw_code)
        b = cls.from_list(matrix)
        return b

    def as_matrix(self):
        matrix = []
        for column in self.columns:
            matrix.append(column.column)
        return matrix

    def add(self, index, char):
        self.columns[index].add(char)
        return self
    
    def is_full(self):
        for column in self.columns:
            if not column.is_full():
                return False
        return True
    
    def _vertical_victory(self, char):
        for column in self.columns:
            if column.is_victory(char):
                return True
        return False
    
    def _horizontal_victory(self, char):
        matrix = transpose_matrix(self.columns)
        board = SquareBoard.from_list(matrix)
        return board._vertical_victory(char)

    def _rising_victory(self, char):
        matrix = invert_matrix(self.columns)
        board = SquareBoard.from_list(matrix)
        return board._descending_victory(char)

    def _descending_victory(self, char):
        matrix = rot_matrix_ccw(self.columns)
        board = SquareBoard.from_list(matrix)
        return board._horizontal_victory(char)

    def is_tie(self, char1, char2):
        if self.is_full():
            if self.is_victory(char1) or self.is_victory(char2):
                return False
            return True
        return False

    def is_victory(self, char):
        if self._vertical_victory(char) or self._horizontal_victory(char) or self._descending_victory(char) or self._rising_victory(char):
            return True
        return False
    
    def as_code(self):
        return BoardCode(self)
    

class BoardCode:
    
    def __init__(self, board):
        self._raw_code = collapse_matrix(board.as_matrix())
    
    @property
    def raw_code(self):
        return self._raw_code
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._raw_code == other._raw_code
    
    def __hash__(self):
        return hash(self._raw_code)

    def __repr__(self):
        return self.raw_code
    
    @classmethod
    def from_raw_code(cls, raw_code):
        code = cls(SquareBoard())
        code._raw_code = raw_code
        return code

    def symmetric(self):
        """
        returns the boardcode reflected in the y axis
        """
        matrix = explode_to_matrix(self.raw_code)
        matrix = matrix[::-1]
        sym_raw_code = collapse_matrix(matrix)
        b = BoardCode.from_raw_code(sym_raw_code)
        return b