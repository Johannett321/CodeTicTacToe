import numpy as np


class LogicChecker:
    def get_winner(self, positions):
        winning_status = self.check_draw(positions)
        if winning_status != 0 and winning_status is not None:
            return winning_status

        winning_status = self.check_diagonals(positions)
        if winning_status != 0 and winning_status is not None:
            return winning_status

        winning_status = self.loop_through_rows(positions)
        if winning_status != 0 and winning_status is not None:
            return winning_status

        positions = np.rot90(positions)
        winning_status = self.loop_through_rows(positions)
        return winning_status

    def loop_through_rows(self, positions):
        for row in positions:
            winning_status = self.check_row(row)
            if winning_status != 0:
                return winning_status

    def check_row(self, row):
        print(f"Checking row:{row}")
        zeros = 0
        ones = 0
        twos = 0
        for cell in row:
            if cell == 0:
                zeros += 1
            if cell == 1:
                ones += 1
            if cell == 2:
                twos += 1
        if ones == 3:
            return 1
        elif twos == 3:
            return 2
        return 0

    def check_diagonals(self, board):
        center = board[1][1]
        if center != 0:
            if board[0][0] == center and board[2][2] == center:
                return center
            elif board[0][2] == center and board[2][0] == center:
                return center
        return 0

    def check_draw(self, board):
        for row in board:
            for cell in row:
                if cell == 0:
                    return 0
        return 3
