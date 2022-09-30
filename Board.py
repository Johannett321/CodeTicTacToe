import random
import time
from tkinter import *
from PIL import Image, ImageTk

from LogicChecker import LogicChecker
from Opponent import Opponent


class Board:
    def __init__(self, window, game_box, opponent):
        self.logic_checker = LogicChecker()
        self.positions = [[0] * 3 for _ in range(3)]
        self.btn_array = [[None] * 3 for _ in range(3)]
        self.game_box = None
        self.window = None
        self.turn = 1
        self.opponent = opponent

        print("Initiated board")
        self.game_box = game_box
        self.window = window

    def draw_board(self):
        print("Drawing board")
        for current_row_index in range(len(self.positions)):
            for current_column_index in range(len(self.positions[current_row_index])):
                self.draw_single_tile(current_row_index, current_column_index, None)

    def draw_single_tile(self, row, column, image):
        # Position image on button
        width = 3
        height = 3
        xpos = (column + 1) * (width * 20)
        ypos = (row + 1) * (height * 19)
        print(f"xPos:{xpos}, yPos:{ypos}")
        if image is None:
            self.btn_array[row][column] = Button(self.game_box, width=width, height=height,
                                                 command=lambda: self.tile_pressed(row, column))
        else:
            self.btn_array[row][column] = Button(self.game_box, width=width * 18, height=height * 18, image=image,
                                                 command=lambda: self.tile_pressed(row, column))
        self.btn_array[row][column].place(x=xpos, y=ypos)

    def remove_single_tile(self, row, column):
        self.btn_array[row][column].destroy()

    def tile_pressed(self, row, column):
        if self.turn == 1:
            self.place_x_in_board_tile(row, column)
        elif self.turn == 2 and self.opponent.can_click:
            self.opponent_place_o(row, column)

    def place_x_in_board_tile(self, row, column):
        if self.turn is not 1:
            return
        self.turn = 2
        self.window.change_status_title(self.opponent.current_name + "'s turn")

        self.positions[row][column] = 1
        self.place_image_in_button(row, column, "images/cross.png")

        if self.check_winning_status() is True:
            self.game_box.after(12000, self.window.show_main_menu)
            return
        self.opponent.play(self)

    def opponent_place_o(self, row, column):
        if self.turn is not 2:
            return
        self.window.change_status_title("Player 1's turn")
        self.turn = 1
        self.positions[row][column] = 2

        self.place_image_in_button(row, column, "images/circle.png")

        if self.check_winning_status() is True:
            if self.opponent.can_click:
                self.game_box.after(12000, self.window.show_main_menu)
            else:
                self.game_box.after(5000, self.window.show_main_menu)
            return
        self.turn = 1

    def place_image_in_button(self, row, column, path):
        load = Image.open(path)
        load = load.resize((45, 45))
        render = ImageTk.PhotoImage(load)

        # Position image on button
        self.remove_single_tile(row, column)
        self.draw_single_tile(row, column, render)
        self.btn_array[row][column].image = render

        self.window.audio_player.play_pop_sound_effect()

    def check_winning_status(self):
        winner = self.logic_checker.get_winner(self.positions)
        if winner != 0 and winner is not None:
            print("STOPPING MUSIC")
            self.window.audio_player.stop_music()

        if winner == 1:
            self.window.change_status_title("You won!")
            self.window.audio_player.play_winning_music()
            return True
        elif winner == 2:
            self.window.change_status_title(self.opponent.current_name + " won!")
            if self.opponent.can_click:
                self.window.audio_player.play_winning_music()
            else:
                self.window.audio_player.play_losing_music()
            return True
        elif winner == 3:
            self.window.change_status_title("Draw!")
            self.window.audio_player.play_losing_music()
            return True
        else:
            return False
