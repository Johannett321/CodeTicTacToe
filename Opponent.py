import random


class Opponent:
    names = ("Eric", "Mary", "Jennifer", "John", "Robert", "Michael", "David", "William", "Thomas",
             "Daniel", "Matthew", "Steven", "Paul", "Christopher", "Linda", "Susan", "Sarah", "Lisa",
             "Nancy", "Betty", "Sandra", "Emily", "Michelle", "Amanda", "Rebecca", "Edward", "George")

    def __init__(self):
        self.can_click = False
        self.isOnline = False
        self.current_name = self.names[random.randint(0, len(self.names) - 1)]

    # The algorithm is asked to play, place the 'o'
    def play(self, board, just_chose=None, just_won=False):
        def place_o():
            # Let the algorithm decide where to play, and place the 'o' there.
            row_col = self.algorithm_decide_position(board)
            board.opponent_place_o(row_col[0], row_col[1])

        # Wait for UI to load
        board.game_box.after(2000, place_o)

    # Let the algorithm decide where to place the 'o'
    def algorithm_decide_position(self, board):
        # Create a matrix of scores for each tile
        positions_scores = [[0] * 3 for _ in range(3)]
        # Calculate a score for every tile
        for row_index in range(0, len(positions_scores)):
            for col_index in range(0, len(positions_scores[row_index])):
                # Tile is already selected, give that tile a very low score
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

                # ROW SCAN: If other tiles in that row is selected by me or opponent, score higher
                for row_scanner_index in range(0, len(positions_scores[row_index])):
                    if board.positions[row_index][row_scanner_index] == 2:
                        if row_scanner_index is not col_index:
                            selected_in_row += 1
                    elif board.positions[row_index][row_scanner_index] == 1:
                        if row_scanner_index is not col_index:
                            opponent_in_row += 1

                # COLUMN SCAN: If other tiles in that column is selected by me or opponent, score higher
                for col_scanner_index in range(0, len(positions_scores)):
                    if board.positions[col_scanner_index][col_index] == 2:
                        if col_scanner_index is not row_index:
                            selected_in_col += 1
                    elif board.positions[col_scanner_index][col_index] == 1:
                        if col_scanner_index is not row_index:
                            opponent_in_col += 1

                # Score diagonals as well
                if (row_index is col_index) or (row_index == 0 and col_index == 2) or (
                        row_index == 2 and col_index == 0):
                    # Score tile higher if other tiles are selected in same diagonals
                    for index in range(0, 3):
                        if (row_index is not index) and (col_index is not index):  # Don't include current tile
                            # Score left diagonals
                            if board.positions[index][index] == 1:
                                opponent_in_ldia += 1
                            elif board.positions[index][index] == 2:
                                selected_in_ldia += 1

                        # Score right diagonals
                        if board.positions[index][2 - index] == 1:
                            opponent_in_rdia += 1
                        elif board.positions[index][2 - index] == 2:
                            selected_in_rdia += 1

                # If i, or the opponent have more than one tile, we should select this tile, score high!.
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

        # Print the algorithms scores
        print("---------- Algorithm scored tiles ----------")
        print("Info: Algorithm randomly makes a bad decision on purpose")
        for row in positions_scores:
            print(row)

        # Determine the tile with the highest score, and choose that
        current_best_score = -5
        should_choose_row = 0
        should_choose_col = 0
        # Loop through all tiles and find highest score
        for row_index in range(0, len(positions_scores)):
            for col_index in range(0, len(positions_scores[row_index])):
                if positions_scores[row_index][col_index] > current_best_score:
                    current_best_score = positions_scores[row_index][col_index]
                    should_choose_row = row_index
                    should_choose_col = col_index

        # If current best score is 0, randomize selection
        if current_best_score == 0:
            def get_random():
                # Choose a random tile
                rand_row = random.randint(0, 2)
                rand_col = random.randint(0, 2)

                # Make sure tile is not already taken
                if board.positions[rand_row][rand_col] == 0:
                    return [rand_row, rand_col]
                else:
                    return get_random()

            # Return a random tile
            return get_random()

        # Return tile with best score
        return [should_choose_row, should_choose_col]
