from Opponent import Opponent


class COOPOpponent(Opponent):

    def __init__(self):
        self.current_name = "Player 2"
        self.can_click = True
        self.isOnline = False

    def play(self, board):
        return
