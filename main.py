import time
from tkinter import *
from PIL import Image, ImageTk

from board import Board


class Window(Frame):
    board = None
    game_box = None
    holder = None

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

    def add_board(self, board:Board):
        self.board = board
        print(f"Added board: {self.board.positions}")

    def draw_board(self):
        print("Drawing board")
        title = Label(self.game_box, text="Welcome to CodeTTT", font=("Calibra", 26, "bold"))
        title.pack()
        self.draw_board_tile()

    def place_x_in_board_tile(self):
        # Create a photoimage object of the image in the path
        load = Image.open("images/cross.png")
        render = ImageTk.PhotoImage(load)

        # Position image on button
        btn = Button(app.game_box, image=render).pack()
        btn.image = render
        btn.place(x=0, y=0)

root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.geometry("1000x600")


def show_menu():
    title = Label(app.game_box, text="Welcome to CodeTTT", font=("Calibra", 26, "bold"))
    title.pack()

    singleplayer_button = Button(app.game_box, text="Singleplayer", command=run_game)
    singleplayer_button.pack()


def run_game():
    app.clear_canvas()
    my_board = Board()
    app.add_board(my_board)
    app.draw_board()


show_menu()
root.mainloop()
