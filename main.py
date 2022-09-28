import time
from tkinter import *
from PIL import Image, ImageTk


class Window(Frame):
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


root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.geometry("1000x600")


def run_game():
    title = Label(app.game_box, text="Welcome to CodeTTT", font=("Calibra", 26, "bold"))
    title.pack()

    singleplayer_button = Button(app.game_box, text="Singleplayer")
    singleplayer_button.pack()


run_game()
root.mainloop()
