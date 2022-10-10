

class Match():
    
    def __init__(self, player1=None, player2=None):
        self.player1 = player1
        self.player2 = player2
        self.player1.char = "x"
        self.player2.char = "o"
        self.players = {"x" : self.player1, "o" : self.player2}
        self.round_robbin = [self.player1, self.player2]
        self.player1.opponent = self.player2
    
    @property
    def next_player(self):
        next = self.round_robbin[0]
        self.round_robbin.reverse()
        return next
    
    def get_player(self, char):
        return self.players[char]
    
    def get_winner(self, board):
        if board.is_victory(self.player1.char):
            return self.player1
        if board.is_victory(self.player2.char):
            return self.player2
        return None
    
    def is_match_over(self):
        answer = 0
        while answer != "Y" and answer != "N":
            answer = input("Do you want to play again? (Y/N)").upper()
        if answer == "N":
            return True
        else:
            return False

   