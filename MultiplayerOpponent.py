from Opponent import Opponent


class MultiplayerOpponent(Opponent):

    def __init__(self):
        self.current_name = "Player 2"
        self.can_click = True

    def play(self, board):
        return
