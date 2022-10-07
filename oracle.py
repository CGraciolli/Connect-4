from enum import Enum
from square_board import SquareBoard
from settings import BOARD_SIZE
from beautifultable import BeautifulTable

##Enum: Base class for creating enumerated constants
##auto: Instances are replaced with an appropriate value for Enum members. By default, the initial value starts at 1.
class ColumnClassification(Enum):
    FULL = -1000
    REALLY_BAD = -10
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
    
    def backtrack(self, list_of_moves):
        pass

    def update_to_bad(self, move):
        pass
    
    def get_help(self):
        pass

    def no_good_options(self, board, player):
        pass

    def make_key(self, board_code, char):
        pass

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
                return ColumnRecommendation(index, ColumnClassification.REALLY_BAD)
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
            elif r == ColumnClassification.REALLY_BAD:
                table.columns.append(["lose"], header=str(index))
        print(table)
    
    def no_good_options(self, board, player):
        rec = self.get_recommendation(board, player.char)
        rec = list(filter(lambda x : x.classification == ColumnClassification.MAYBE or x.classification == ColumnClassification.WIN, rec))
        return rec == []

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
    
    def update_to_bad(self, move):
        ##create key
        key = self.make_key(move.board_code, move.player.char)
        ##get wrong classification
        board = SquareBoard.from_code(move.board_code)
        rec = self.get_recommendation(board, move.player.char)
        ##correct it
        rec[move.position] = ColumnRecommendation(move.position, ColumnClassification.BAD)
        self.past_rec[key] = rec
    
    def backtrack(self, list_of_moves):
        """
        reexamines all moves
        if it finds one where all is lost,
        the one beore that is updates to bad
        """
        print("Learning...")
        for move in list_of_moves:
            self.update_to_bad(move)
            board = SquareBoard.from_code(move.board_code)
            if not self.no_good_options(board, move.player):
                break
        print("Size of knowledge base: ", len(self.past_rec))