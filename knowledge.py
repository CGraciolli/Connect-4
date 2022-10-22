

class Knowledge:
    """
    contains a dictionary whose keys are made combining the board code and the player´s character
    and the values are the recommendations
    """
    
    def __init__(self, past_rec={}):
        self.past_rec = past_rec
    
    def __len__(self):
        return len(self.past_rec.keys())
    
