from copy import deepcopy
from enum import Enum
from square_board import SquareBoard
from settings import BOARD_SIZE
from beautifultable import BeautifulTable

##Enum: Base class for creating enumerated constants
##auto: Instances are replaced with an appropriate value for Enum members. By default, the initial value starts at 1.
class ColumnClassification(Enum):
    FULL = -1000
    BAD = 1
    MAYBE = 10
    WIN = 100

class ColumnRecommendation:
   
   def __init__(self, index, classification):
        self.index = index
        self.classification = classification
        
   def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.classification == other.classification
        return False

   def __hash__(self) -> int:
        return hash(self.index, self.classification)
        
class BaseOracle:
    """
    recives a square board
    for each column, determines if it is full or not
    """
    def get_recommendation(self, board, char):
        recommendations = []
        for i in range(len(board.columns)):
            recommendations.append(self.get_column_recommendation(board, i, char))
        return recommendations

    def get_column_recommendation(self, board, index, char):
        """
        classifies a column as either FULL or MAYBE
        """
        column = board.columns[index]
        if column.is_full():
            return ColumnRecommendation(index, ColumnClassification.FULL)
        return ColumnRecommendation(index, ColumnClassification.MAYBE)

class SmartOracle(BaseOracle):
    
    def get_column_recommendation(self, board, index, char):
        """
        classifies a column as FULL, MAYBE, WIN or LOSE
        """
        column = board.columns[index]
        if column.is_full():
            return ColumnRecommendation(index, ColumnClassification.FULL)
        else:
            if board.is_winning_move(index, char):
                return ColumnRecommendation(index, ColumnClassification.WIN)
            elif board.is_losing_move(index, char):
                return ColumnRecommendation(index, ColumnClassification.BAD)
            else:
                return ColumnRecommendation(index, ColumnClassification.MAYBE)
    
    def get_help(self, board, char):
        table = BeautifulTable()
        for index in range(BOARD_SIZE):
            r = self.get_column_recommendation(board, index, char).classification
            if r == ColumnClassification.FULL:
                table.columns.append(["full"], header=str(index))
            elif r == ColumnClassification.MAYBE:
                table.columns.append(["maybe"], header=str(index))
            elif r == ColumnClassification.BAD:
                table.columns.append(["bad"], header=str(index))
            elif r == ColumnClassification.WIN:
                table.columns.append(["win"], header=str(index))
        print(table)
    
    def no_good_options(self, board, player):
        ##True if for every move, there is a possible move for the opponent such that every following move is a losing (BAD) move
        answer = True
        for index in range(BOARD_SIZE):
            temp = deepcopy(board)
            temp.add(index, player.char)
            bad_move = True
            for j in range(BOARD_SIZE):
                temp_j = deepcopy(temp)
                temp_j.add(j, player.opponent.char)
                good_move = True ##the opponent playing in the position j is a good move (for them), if after there are only losing moves for our player
                for k in range(BOARD_SIZE):
                    good_move = good_move and temp_j.is_losing_move(k, player.char)
            bad_move = bad_move and good_move ##playing at index is a bad move if every possibe move for the opponent is a good move
            answer = answer and bad_move ##there are no good option if all possible moves are bad moves
        return answer
        
class MemoizingOracle(SmartOracle):
    """
    get_recommendation is memoized
    """

    def __init__(self):
        super().__init__
        self.past_rec = {}

    def get_recommendation(self, board, char):
        key = self.make_key(board.as_code(), char)
        if key not in self.past_rec:
            self.past_rec[key] = super().get_recommendation(board, char)
        return self.past_rec[key]
    
    def make_key(self, board_code, char):
        key = board_code.raw_code + char
        return key
    
    

class LearningOracle(MemoizingOracle):
    
    def update_to_bad(self, board_code, player, position):
        ##create key
        key = self.make_key(board_code, player.char)
        ##get wrong classification
        board = SquareBoard.from_code(board_code)
        rec = self.get_recommendation(board, player.char)
        ##correct it
        rec[position] = ColumnRecommendation(position, ColumnClassification.BAD)
        self.past_rec[key] = rec