from tkinter import *
from PIL import Image, ImageTk

from LogicChecker import LogicChecker


class Board:
    def __init__(self, window, game_box, opponent, who_starts=1):
        self.logic_checker = LogicChecker()
        self.positions = [[0] * 3 for _ in range(3)]
        self.btn_array = [[None] * 3 for _ in range(3)]
        self.game_box = None
        self.window = None
        self.turn = who_starts
        self.opponent = opponent

        self.game_box = game_box
        self.window = window

    # Creates the tiles
    def draw_board(self):
        for current_row_index in range(len(self.positions)):
            for current_column_index in range(len(self.positions[current_row_index])):
                self.draw_single_tile(current_row_index, current_column_index, None)
        if self.turn == 2:
            self.opponent.play(self)

    # Create one tile either with or without circle/x inside
    def draw_single_tile(self, row, column, image):
        width = 3
        height = 3
        xpos = (column + 1) * (width * 20)
        ypos = (row + 1) * (height * 19)
        if image is None:  # Empty tile
            self.btn_array[row][column] = Button(self.game_box, width=width, height=height,
                                                 command=lambda: self.tile_pressed(row, column))
        else:  # Tile has been selected by someone
            self.btn_array[row][column] = Button(self.game_box, width=width * 18, height=height * 18, image=image,
                                                 command=lambda: self.tile_pressed(row, column))
        self.btn_array[row][column].place(x=xpos, y=ypos)

    # Destroys one tile
    def remove_single_tile(self, row, column):
        self.btn_array[row][column].destroy()

    # Tile is pressed: place x or o in it
    def tile_pressed(self, row, column):
        if self.turn == 1:
            self.place_x_in_board_tile(row, column)
        elif self.turn == 2 and self.opponent.can_click:
            self.opponent_place_o(row, column)

    # Places an x in a board tile
    def place_x_in_board_tile(self, row, column):
        def ui_done():  # Let the opponent play
            self.opponent.play(self, str(row) + ";" + str(column))

        # Do not place X if it's not my turn
        if self.turn != 1:
            return

        # Do not allow selecting that tile if it's already taken
        if self.positions[row][column] != 0:
            return

        # Switch turn
        self.turn = 2
        self.window.change_status_title(self.opponent.current_name + "'s turn")

        # Select the tile I selected
        self.positions[row][column] = 1
        self.place_image_in_button(row, column, "images/cross.png")

        # Have i won?
        if self.check_winning_status() is True:
            if self.opponent.isOnline:  # Make sure the opponent is informed that i won
                self.opponent.play(self, str(row) + ";" + str(column), True)

            # Show main menu
            self.game_box.after(12000, self.window.show_main_menu)
            return

        # Let UI finish before opponent play
        self.window.after(1000, ui_done)

    # Place an o as the opponent
    def opponent_place_o(self, row, column):
        # Make sure it actually is the opponents turn
        if self.turn != 2:
            return

        # Make sure the tile has not already been selected
        if self.positions[row][column] != 0:
            return

        # Change turn
        self.window.change_status_title("Your turn")
        self.turn = 1

        # Select the tile the opponent choose
        self.positions[row][column] = 2
        self.place_image_in_button(row, column, "images/circle.png")

        # Has someone won?
        if self.check_winning_status() is True:
            if self.opponent.can_click:  # If we are playing on the same machine
                self.game_box.after(12000, self.window.show_main_menu)
            else:  # If the opponent is on another machine
                self.game_box.after(5000, self.window.show_main_menu)
            return

    # Place X or O in a button
    def place_image_in_button(self, row, column, path):
        # Load the image
        load = Image.open(path)
        load = load.resize((45, 45))
        render = ImageTk.PhotoImage(load)

        # Position image on button
        self.remove_single_tile(row, column)
        self.draw_single_tile(row, column, render)
        self.btn_array[row][column].image = render

        # Play pop
        self.window.audio_player.play_pop_sound_effect()

    # Determine if someone has won
    def check_winning_status(self):
        # Check if someone has won
        winner = self.logic_checker.get_winner(self.positions)
        if winner != 0 and winner is not None:
            # Someone just won the game
            self.window.audio_player.stop_music()

        if winner == 1:  # The winner is me
            self.window.change_status_title("You won!")
            self.window.audio_player.play_winning_music()
            return True
        elif winner == 2:  # The winner is the opponent
            self.window.change_status_title(self.opponent.current_name + " won!")
            if self.opponent.can_click:  # Local machine or network?
                self.window.audio_player.play_winning_music()
            else:
                self.window.audio_player.play_losing_music()
            return True
        elif winner == 3:  # Draw
            self.window.change_status_title("Draw!")
            self.window.audio_player.play_losing_music()
            return True
        else:
            return False
