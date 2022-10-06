from oracle import MemoizingOracle
from oracle import BaseOracle, ColumnClassification
from settings import BOARD_SIZE
from random import choice
from move import Move
from collections import deque

class Player:
    def __init__(self, name, char = None, oracle = BaseOracle(), opponent = None):
        self.name = name
        self.char = char
        self.oracle = oracle
        self._opponent = opponent
        self.last_move = deque([])
    
    @property
    def opponent(self):
        return self._opponent
    
    @opponent.setter
    def opponent(self, other):
        if other != None:
            self._opponent = other
            other._opponent = self
    
    def choose(self, recommendations):
        """
        is given recommendations by the oracle and chooses the best one
        """
        available_choices = list(filter(lambda x: x.classification != ColumnClassification.FULL, recommendations))
        available_choices = sorted(available_choices, key = lambda x : x.classification.value, reverse = True)
        if available_choices[0].classification == available_choices[-1].classification:
            pick = choice(available_choices)
        else:
            pick = available_choices[0]
        return pick.index
        
    def play(self, board):
        """
        places piece in the first available column
        """
        move = self.ask_oracle(board)
        board_after_move = self.play_on(board, move)
        return board_after_move
    
    def play_on(self, board, index):
        board.add(index, self.char)
        board_code = board.as_code()
        rec = self.oracle.get_recommendation(board, self.char)
        self.last_move.appendleft(Move(index, board_code, rec, self))
        return board
    
    def ask_oracle(self, board):
        """
        is given a board and asks the oracle for recommendations
        """
        recommendations = self.oracle.get_recommendation(board, self.char)
        best = self.choose(recommendations)
        return best
    
    def on_win(self):
        pass

    def on_lose(self):
        pass

##validation functions

def is_int(n):
    """
    recieves a string and checks if it represents a integer
    """
    try:
        int(n)
        return True
    except:
        return False

def is_within_range(board, n):
    """
    recieves a square board and an integer,
    checks if the integer is within range of the board's columns
    """
    if n >= 0 and n < BOARD_SIZE:
        return True
    return False

def is_column_not_full(board, index):
    """
    recieves a square board and an integer,
    checks if the column associated with the integer is available
    """
    return not board.columns[index].is_full()

class HumanPlayer(Player):
    
    def __init__(self, name, char = None, oracle=MemoizingOracle()):
        super().__init__(name, char, oracle)

    def ask_oracle(self, board):
        ##the oracle is the human
        while True:
            answer = input("Select a column (or press h for help): ")
            if answer == "h":
                self.oracle.get_help(board, self.char)
            if is_int(answer):
                answer = int(answer)
                if is_within_range(board, answer) and is_column_not_full(board, answer):
                    return answer

class ReportingPlayer(Player):

    def on_lose(self):
        board_code = self.last_move[0].board_code
        position = self.last_move[0].position
        self.oracle.update_to_bad(board_code, self, position)