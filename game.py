from pyfiglet import Figlet
from enum import Enum, auto
from match import Match
from player import HumanPlayer, ReportingPlayer, Player
from square_board import SquareBoard
from list_tools import invert_matrix
from beautifultable import BeautifulTable
from settings import BOARD_SIZE
from oracle import MemoizingOracle, LearningOracle

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
        self.start_game_loop()
    
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
        while resposta != 1 and resposta != 2:
            resposta = int(input("Please type 1 or 2: "))
        if resposta == 1:
            self.round_type = RoundType.COMPUTER_VS_COMPUTER
        if resposta == 2:
            self.round_type = RoundType.COMPUTER_VS_HUMAN

    def get_difficulty_level(self):
        print("Select difficulty level:\n1.Easy\n2.Medium\n3.Hard\n4.Very Hard")
        resposta = 0
        while resposta != 1 and resposta != 2 and resposta != 3 and resposta != 4:
            resposta = int(input("Please type 1, 2, 3 or 4: "))
        if resposta == 1:
            self.difficulty_level = DifficultyLevel.EASY
        elif resposta == 2:
            self.difficulty_level = DifficultyLevel.MEDIUM
        elif resposta == 3:
            self.difficulty_level = DifficultyLevel.HARD
        elif resposta == 4:
            self.difficulty_level = DifficultyLevel.VERY_HARD

    def make_match(self):
        if self.difficulty_level == DifficultyLevel.EASY:
            player1 = Player("Jaco")
        elif self.difficulty_level == DifficultyLevel.MEDIUM:
            player1 = ReportingPlayer("Jaco", oracle = MemoizingOracle())
        elif self.difficulty_level == DifficultyLevel.HARD:
            player1 = ReportingPlayer("Jaco", oracle = LearningOracle())
        elif self.difficulty_level == DifficultyLevel.VERY_HARD:
            player1 = ReportingPlayer("Jaco", oracle = LearningOracle())
            get_base_knowledge(20, player1, ReportingPlayer("Lua", oracle = LearningOracle()))
        if self.round_type == RoundType.COMPUTER_VS_COMPUTER:
            player2 = ReportingPlayer("Lua", oracle = LearningOracle())
            player1 = ReportingPlayer("Jaco", oracle = LearningOracle())
        if self.round_type == RoundType.COMPUTER_VS_HUMAN:
            player2 = HumanPlayer(input("Enter your name: "))
        return Match(player1, player2)
    
    def start_game_loop(self):
        go_on = True
        while go_on:
            ##gets player who goes next
            current_player = self.match.next_player
            ##they play
            current_player.play(self.board)
            ##shows move
            self.display_move(current_player)
            ##prints board
            self.display_board()
            ##checks if the match is over
            if self.has_winner_or_is_a_tie():
                self.display_result()
                is_it_over = self.match.is_match_over()
                if not is_it_over:
                    self.board = SquareBoard()
                    self.display_board()
                else:
                    go_on = False
    
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

    
    def has_winner_or_is_a_tie(self):
        if self.board.is_victory("x") or self.board.is_victory("o") or self.board.is_tie("x", "o"):
            winner = self.match.get_winner(self.board)
            if winner != None:
                winner.on_win()
                winner.opponent.on_lose()
            return True
        return False

    def display_result(self):
        winner = self.match.get_winner(self.board)
        if winner:
            print(winner.name, "won!")
        else:
            print("The match ended in a tie.")

def get_base_knowledge(n, player1, player2):
    """
    recives two players
    creates n matches between them
    merges their knowledges into player 1´s oracle"""
    Match(player1, player2)
    for _ in range(n):
        Match(player1, player2)
    base_knowledge = player1.oracle.knowledge.merge(player2.oracle.knowledge)
    return base_knowledge