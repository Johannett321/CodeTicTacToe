import random


class Opponent:
    names = ("Stian", "Jan", "Hans", "Jens")

    def __init__(self):
        self.can_click = False
        self.isOnline = False
        self.current_name = self.names[random.randint(0, len(self.names)-1)]

    def play(self, board, just_chose=None, just_won=False):
        def place_o():
            row_col = self.algorithm_decide_position(board)
            board.opponent_place_o(row_col[0], row_col[1])
        board.game_box.after(2000, place_o)

    def algorithm_decide_position(self, board):
        positions_scores = [[0] * 3 for _ in range(3)]
        # Calculate a score for every cell
        for row_index in range(0, len(positions_scores)):
            for col_index in range(0, len(positions_scores[row_index])):
                if board.positions[row_index][col_index] == 1 or board.positions[row_index][col_index] == 2:
                    positions_scores[row_index][col_index] = -1000
                    continue

                # Rows and columns
                selected_in_row = 0
                selected_in_col = 0
                opponent_in_row = 0
                opponent_in_col = 0

                # Left and right diagonals
                selected_in_ldia = 0
                selected_in_rdia = 0
                opponent_in_ldia = 0
                opponent_in_rdia = 0

                # Scan all the other cells in the same row. Who owns them?
                for row_scanner_index in range(0, len(positions_scores[row_index])):
                    if board.positions[row_index][row_scanner_index] == 2:
                        if row_scanner_index is not col_index:
                            selected_in_row += 1
                    elif board.positions[row_index][row_scanner_index] == 1:
                        if row_scanner_index is not col_index:
                            opponent_in_row += 1

                # Scan all the other cells in the same column. Who owns them?
                for col_scanner_index in range(0, len(positions_scores)):
                    if board.positions[col_scanner_index][col_index] == 2:
                        if col_scanner_index is not row_index:
                            selected_in_col += 1
                    elif board.positions[col_scanner_index][col_index] == 1:
                        if col_scanner_index is not row_index:
                            opponent_in_col += 1

                # Check diagonals
                if (row_index is col_index) or (row_index == 0 and col_index == 2) or (row_index == 2 and col_index == 0):
                    print("----------- CHECKING DIAS ----------------")
                    for index in range(0, 3):
                        print("Index_ " + str(index))
                        if (row_index is not index) and (col_index is not index):  # Don't include current cell
                            print("PASSED")
                            if board.positions[index][index] == 1:
                                opponent_in_ldia += 1
                            elif board.positions[index][index] == 2:
                                selected_in_ldia += 1

                        print("Checking rdia: " + str(index) + str(2 - index) + ", value: " + str(
                            board.positions[index][2 - index]))
                        if board.positions[index][2 - index] == 1:
                            opponent_in_rdia += 1
                            print("Requirements met! Op's in rdia: " + str(opponent_in_rdia))
                        elif board.positions[index][2 - index] == 2:
                            selected_in_rdia += 1

                # If i, or the opponent have more than 1 cell, we should take that.
                if row_index is col_index and row_index != 1:
                    if selected_in_ldia > 1:
                        positions_scores[row_index][col_index] = 1000
                    elif opponent_in_ldia > 1:
                        positions_scores[row_index][col_index] = 500
                elif row_index == 1 and col_index == 1:
                    if selected_in_ldia > 1 or selected_in_rdia > 1:
                        positions_scores[row_index][col_index] = 1000
                    elif opponent_in_ldia > 1 or opponent_in_rdia > 1:
                        positions_scores[row_index][col_index] = 500
                elif (row_index == 0 and col_index == 2) or (row_index == 2 and col_index == 0):
                    if selected_in_rdia > 1 or opponent_in_rdia > 1:
                        positions_scores[row_index][col_index] = 1000
                elif selected_in_row > 1 or selected_in_col > 1 or opponent_in_col > 1 or opponent_in_row > 1:
                    positions_scores[row_index][col_index] = 1000
                else:
                    positions_scores[row_index][col_index] = selected_in_row + selected_in_col

        print("Scores:")
        for row in positions_scores:
            print(row)

        current_best_score = -5
        should_choose_row = 0
        should_choose_col = 0
        for row_index in range(0, len(positions_scores)):
            for col_index in range(0, len(positions_scores[row_index])):
                if positions_scores[row_index][col_index] > current_best_score:
                    current_best_score = positions_scores[row_index][col_index]
                    should_choose_row = row_index
                    should_choose_col = col_index

        # Randomize selection
        if current_best_score == 0:
            print(board.positions)
            def get_random():
                rand_row = random.randint(0, 2)
                rand_col = random.randint(0, 2)
                print(str(rand_row) + str(rand_col))
                if board.positions[rand_row][rand_col] == 0:
                    return [rand_row, rand_col]
                else:
                    return get_random()
            return get_random()

        return [should_choose_row, should_choose_col]
