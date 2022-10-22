from enum import Enum
from square_board import SquareBoard
from settings import BOARD_SIZE
from beautifultable import BeautifulTable
from copy import deepcopy
from knowledge import Knowledge

##Enum: Base class for creating enumerated constants
##auto: Instances are replaced with an appropriate value for Enum members. By default, the initial value starts at 1.
class ColumnClassification(Enum):
    FULL = -1000
    REALLY_BAD = -10
    BAD = 1
    MAYBE = 10
    GOOD = 20
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
    
   def __repr__(self):
        return str(self.classification)
        
class BaseOracle:
    """
    recives a square board
    for each column, determines if it is full or not
    """

    def __init__(self, knowledge=Knowledge()):
        self.knowledge = knowledge

    def get_recommendation(self, board, char): ##should recive board_code in the future
        recommendations = []
        for i in range(BOARD_SIZE):
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
    
    def backtrack(self, list_of_moves, lost):
        pass

    def update_to_bad(self, move):
        pass
    
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
            elif r == ColumnClassification.GOOD:
                table.columns.append(["good"], header=str(index))
        print(table)

    def no_good_options(self, board, player):
        pass

    def make_key(self, board_code, char):
        pass

    def make_swapped_key(self, board_code, char):
        pass

    def is_winning_move(self, board, index, char):
        pass

    def is_losing_move(self, board, index, char):
        pass

    def only_good_options(self, board, player):
        pass

    def update_to_good(self, move):
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
            if self.is_winning_move(board, index, char):
                return ColumnRecommendation(index, ColumnClassification.WIN)
            elif self.is_losing_move(board, index, char):
                return ColumnRecommendation(index, ColumnClassification.REALLY_BAD)
            else:
                return ColumnRecommendation(index, ColumnClassification.MAYBE)
    
    
    def no_good_options(self, board, player):
        rec = self.get_recommendation(board, player.char)
        rec = list(filter(lambda x : x.classification == ColumnClassification.MAYBE or x.classification == ColumnClassification.WIN or x.classification == ColumnClassification.GOOD, rec))
        return rec == []
    
    def only_good_options(self, board, player):
        rec = self.get_recommendation(board, player.char)
        rec = list(filter(lambda x : x.classification == ColumnClassification.FULL or x.classification == ColumnClassification.REALLY_BAD or x.classification == ColumnClassification.BAD, rec))
        return rec == []
    
    def is_winning_move(self, board, index, char):
        temp = deepcopy(board)
        temp.add(index, char)
        return temp.is_victory(char)
    
    def is_losing_move(self, board, index, char):
        if char == "x":
            other_char = "o"
        if char == "o":
            other_char = "x"
        temp = deepcopy(board)
        temp.add(index, char)
        for i in range(BOARD_SIZE):
            if self.is_winning_move(temp, i, other_char):
                return True
        return False

class MemoizingOracle(SmartOracle):
    """
    get_recommendation is memoized
    """

    def get_recommendation(self, board, char):
        ##needs to check the same board with opposite pieces (both times)
        key = self.make_key(board.as_code(), char)
        swapkey = self.make_swapped_key(board.as_code(), char)
        symkey = self.make_key(board.as_code().symmetric(), char)
        swapsymkey =  self.make_swapped_key(board.as_code().symmetric(), char)
        if key not in self.knowledge.past_rec and symkey not in self.knowledge.past_rec and swapkey not in self.knowledge.past_rec and swapsymkey not in self.knowledge.past_rec:
            self.knowledge.past_rec[key] = super().get_recommendation(board, char)
        if key in self.knowledge.past_rec:
            return self.knowledge.past_rec[key]
        elif symkey in self.knowledge.past_rec:
            recs = self.knowledge.past_rec[symkey]
            rec = []
            for i in range(BOARD_SIZE):
                classification = recs[BOARD_SIZE -1 -i].classification
                rec.append(ColumnRecommendation(i, classification))
            return rec
        elif swapkey in self.knowledge.past_rec:
            return self.knowledge.past_rec[swapkey]
        elif swapsymkey in self.knowledge.past_rec:
            recs = self.knowledge.past_rec[swapsymkey]
            rec = []
            for i in range(BOARD_SIZE):
                classification = recs[BOARD_SIZE -1 -i].classification
                rec.append(ColumnRecommendation(i, classification))
            return rec

    
    def make_key(self, board_code, char):
        key = board_code.raw_code + char
        return key
    
    def make_swapped_key(self, board_code, char):
        board_code = board_code.swapped_code()
        if char == "x":
            key = self.make_key(board_code, "o")
        elif char == "o":
            key = self.make_key(board_code, "x")
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
        self.knowledge.past_rec[key] = rec
    
    def update_to_good(self, move):
        ##create key
        key = self.make_key(move.board_code, move.player.char)
        ##get wrong classification
        board = SquareBoard.from_code(move.board_code)
        rec = self.get_recommendation(board, move.player.char)
        ##correct it
        rec[move.position] = ColumnRecommendation(move.position, ColumnClassification.GOOD)
        self.knowledge.past_rec[key] = rec

    def backtrack(self, list_of_moves, lost):
        """
        reexamines all moves
        if it finds one where all is lost,
        the one beore that is updates to bad
        lost is a boolean that lets us know if we lost
        """
        print("Learning...")
        if lost:
            for move in list_of_moves:
                self.update_to_bad(move)
                board = SquareBoard.from_code(move.board_code)
                if not self.no_good_options(board, move.player):
                    break
        else:
            for move in list_of_moves:
                self.update_to_bad(move)
                board = SquareBoard.from_code(move.board_code)
                if not self.only_good_options(board, move.player):
                    break

        print("Size of knowledge base: ", len(self.knowledge))



    

