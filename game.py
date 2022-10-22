from pyfiglet import Figlet
from enum import Enum, auto

from urllib3 import Retry
from match import Match
from player import HumanPlayer, ReportingPlayer, Player
from square_board import SquareBoard
from list_tools import invert_matrix
from beautifultable import BeautifulTable
from settings import BOARD_SIZE
from oracle import SmartOracle, LearningOracle

class RoundType(Enum):
    COMPUTER_VS_COMPUTER = auto()
    COMPUTER_VS_HUMAN = auto()

class DifficultyLevel(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()
    VERY_HARD = auto()

class Game:
    
    def __init__(self, round_type = RoundType.COMPUTER_VS_COMPUTER, match = Match(ReportingPlayer("R2D2"),ReportingPlayer("C3PO")), difficulty_level = DifficultyLevel.EASY):
        self.round_type = round_type
        self.match = match
        self.board = SquareBoard()
        self.difficulty_level = difficulty_level

    def start(self):
        ##prints logo
        self.print_logo()
        ##match's configuration
        self.configurated_by_user()
        ##starts game loop
        self.start_game_loop(False, 0)
    
    def print_logo(self):
        logo = Figlet(font = "stop", )
        print(logo.renderText("Connect"))
    
    def configurated_by_user(self):
        self.get_round_type()
        if self.round_type == RoundType.COMPUTER_VS_HUMAN:
            self.get_difficulty_level()
        self.match = self.make_match()
    
    def get_round_type(self):
        print("Select round type:\n1.Computer vs computer\n2.Computer vs human")
        resposta = 0
        while resposta != "1" and resposta != "2":
            resposta = input("Please type 1 or 2: ")
        if resposta == "1":
            self.round_type = RoundType.COMPUTER_VS_COMPUTER
        if resposta == "2":
            self.round_type = RoundType.COMPUTER_VS_HUMAN

    def get_difficulty_level(self):
        print("Select difficulty level:\n1.Easy\n2.Medium\n3.Hard\n4.Very Hard")
        resposta = 0
        while resposta != "1" and resposta != "2" and resposta != "3" and resposta != "4":
            resposta = input("Please type 1, 2, 3 or 4: ")
        if resposta == "1":
            self.difficulty_level = DifficultyLevel.EASY
        elif resposta == "2":
            self.difficulty_level = DifficultyLevel.MEDIUM
        elif resposta == "3":
            self.difficulty_level = DifficultyLevel.HARD
        elif resposta == "4":
            self.difficulty_level = DifficultyLevel.VERY_HARD

    def make_match(self):
        if self.difficulty_level == DifficultyLevel.EASY:
            player1 = Player("Jaco")
        elif self.difficulty_level == DifficultyLevel.MEDIUM:
            player1 = Player("Jaco", oracle = SmartOracle())
        elif self.difficulty_level == DifficultyLevel.HARD:
            player1 = ReportingPlayer("Jaco")
        elif self.difficulty_level == DifficultyLevel.VERY_HARD:
            k = self.get_base_knowledge(20)
            player1 = ReportingPlayer("Jaco", oracle = LearningOracle(k))
        if self.round_type == RoundType.COMPUTER_VS_COMPUTER:
            player2 = ReportingPlayer("Lua")
            player1 = ReportingPlayer("Jaco")
        if self.round_type == RoundType.COMPUTER_VS_HUMAN:
            player2 = HumanPlayer(input("Enter your name: "))
        return Match(player1, player2)
    
    def start_game_loop(self, training, n):
        go_on = True
        counter = 0
        while go_on:
            ##gets player who goes next
            current_player = self.match.next_player
            ##they play
            current_player.play(self.board)
            if not training:
                ##shows move
                self.display_move(current_player)
                ##prints board
                self.display_board()
            ##checks if the match is over
            if self.has_winner_or_is_a_tie(training):
                if not training:
                    self.display_result()                
                    is_it_over = self.match.is_match_over()
                else:
                    counter += 1
                    is_it_over = (counter >= n)
                if not is_it_over:
                    self.board = SquareBoard()
                    if not training:
                        self.display_board()
                else: ##if we are here, we are in a training match and it has ended
                    return current_player.oracle.knowledge

    
    def get_base_knowledge(self, n):
        """
        creates n matches
        returns the knowledge acquired in these matches
        """
        Match(ReportingPlayer("Jaco"), ReportingPlayer("Lua"))
        knowledge = self.start_game_loop(True, n)
        self.board = SquareBoard()
        return knowledge 

    def display_move(self, player):
        print(player.name, "placed a piece in column", player.moves[0].position)

    def display_board(self):
        matrix = self.board.as_matrix()
        matrix = invert_matrix(matrix)
        bt = BeautifulTable()
        for column in matrix:
            bt.columns.append(column)
        bt.columns.header = [str(i) for i in range(BOARD_SIZE)]
        print(bt)

    
    def has_winner_or_is_a_tie(self, training):
        if self.board.is_victory("x") or self.board.is_victory("o") or self.board.is_tie("x", "o"):
            winner = self.match.get_winner(self.board)
            if winner != None:
                winner.on_win(training)
                winner.opponent.on_lose(training)
            return True
        return False

    def display_result(self):
        winner = self.match.get_winner(self.board)
        if winner:
            print(winner.name, "won!")
        else:
            print("The match ended in a tie.")

