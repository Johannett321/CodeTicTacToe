import gc
import time
from threading import Thread
from tkinter import *
from PIL import Image, ImageTk

from MultiplayerOpponent import MultiplayerOpponent
from Opponent import Opponent
from Sounds import AudioPlayer
from Board import Board

# _boot_time = 4000
_boot_time = 0


class Window(Frame):
    board = None
    game_box = None
    holder = None
    title = None
    music_thread = None
    audio_player = AudioPlayer()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        load = Image.open("images/background.jpg")
        render = ImageTk.PhotoImage(load)
        img = Label(master=self, image=render)
        img.image = render
        img.place(x=0, y=0)

        self.holder = Frame(self)
        self.holder.pack(padx=120, pady=120)

        self.create_game_box()

    def create_game_box(self):
        self.game_box = Canvas(master=self.holder, width=300, height=300)
        self.game_box.pack_propagate(0)
        self.game_box.pack()

    def clear_canvas(self):
        self.game_box.destroy()
        self.create_game_box()

    def add_board(self, board: Board):
        self.board = board
        print(f"Added board: {self.board.positions}")

    def run_singleplayer_game(self):
        self.audio_player.stop_music()
        self.audio_player.play_battle_music()
        self.clear_canvas()

        self.board = Board(self, self.game_box, Opponent())
        self.title = Label(self.game_box, text="Your turn", font=("Calibra", 26, "bold"))
        self.title.pack(pady=10)
        self.board.draw_board()

    def run_multiplayer_game(self):
        self.audio_player.stop_music()
        self.audio_player.play_battle_music()
        self.clear_canvas()

        self.board = Board(self, self.game_box, MultiplayerOpponent())
        self.title = Label(self.game_box, text="Your turn", font=("Calibra", 26, "bold"))
        self.title.pack(pady=10)
        self.board.draw_board()

    def change_status_title(self, text):
        self.title.config(text=text)

    def show_main_menu(self):
        self.audio_player.play_menu_music()
        self.clear_canvas()
        title = Label(app.game_box, text="Welcome to CodeTTT", font=("Calibra", 26, "bold"))
        title.pack(pady=10)

        singleplayer_button = Button(app.game_box, text="Singleplayer", command=self.run_singleplayer_game)
        singleplayer_button.pack()

        multiplayer_button = Button(app.game_box, text="Co-op", command=self.run_multiplayer_game)
        multiplayer_button.pack(pady=10)

    def show_intro(self):
        self.game_box.destroy()
        title = Label(app, background="green", text="CodeTTT", foreground="white", font=("Calibra", 40, "bold"))
        title.pack(pady=30)
        self.game_box.after(_boot_time, self.show_main_menu)


root = Tk()
root.resizable(width=False, height=False)
app = Window(root)
root.wm_title("CodeTTT")
# root.geometry("1000x600")

# Centering window
window_width = 1000
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

app.show_intro()
root.mainloop()
