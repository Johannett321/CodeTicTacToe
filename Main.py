import random
import time
import tkinter
from tkinter import *
from PIL import Image, ImageTk

from COOPOpponent import COOPOpponent
from MultiplayerOpponent import MultiplayerOpponent
from Opponent import Opponent
from Server import Server
from Sounds import AudioPlayer
from Board import Board

_boot_time = 4000


class Window(Frame):
    board = None
    game_box = None
    holder = None
    title = None
    music_thread = None
    audio_player = AudioPlayer()
    port = random.randint(5000, 9000)

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

    def run_coop_game(self):
        self.audio_player.stop_music()
        self.audio_player.play_battle_music()
        self.clear_canvas()

        self.board = Board(self, self.game_box, COOPOpponent())
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
        singleplayer_button.pack(pady=5)

        multiplayer_button = Button(app.game_box, text="Co-op", command=self.run_coop_game)
        multiplayer_button.pack(pady=5)

        multiplayer_button = Button(app.game_box, text="Join server", command=self.show_multiplayer_menu)
        multiplayer_button.pack(pady=5)

        multiplayer_button = Button(app.game_box, text="Host server", command=self.host_server)
        multiplayer_button.pack(pady=5)

    def host_server(self):
        print("Defining port")
        server = Server(self.port)
        server.start_server()

    def show_multiplayer_menu(self):
        self.clear_canvas()

        self.title = Label(self.game_box, text="Join game", font=("Calibra", 26, "bold"))
        self.title.pack(pady=5)

        ip = tkinter.StringVar()
        port = tkinter.StringVar()
        username = tkinter.StringVar()

        Label(self.game_box, text="What's the ip?", font=("Calibra", 15, "bold")).pack(pady=2)
        ip_input = Entry(app.game_box, textvariable=ip, font=('calibre', 10, 'normal'))
        ip_input.pack(pady=10)

        Label(self.game_box, text="What's the port?", font=("Calibra", 15, "bold")).pack(pady=2)
        port_input = Entry(app.game_box, textvariable=port, font=('calibre', 10, 'normal'))
        port_input.pack(pady=10)

        Label(self.game_box, text="Your name?", font=("Calibra", 15, "bold")).pack(pady=2)
        username_input = Entry(app.game_box, textvariable=username, font=('calibre', 10, 'normal'))
        username_input.pack(pady=10)

        join_button = Button(app.game_box, text="Join", command=lambda: self.join_multiplayer_game(ip.get(), int(port.get()), username.get()))
        join_button.pack(pady=5)

    def join_multiplayer_game(self, ip, port, username):
        def ui_done():
            opponent = MultiplayerOpponent(ip, port)

            opponent.send_command_to_server("MyID")
            opponent.send_command_to_server("MyUsername;" + username)
            server_ready = opponent.send_command_to_server("YouReady?")
            print("Server_ready: " + server_ready)
            while server_ready == "False":
                time.sleep(1)
                server_ready = opponent.send_command_to_server("YouReady?")

            opponent.set_name(server_ready.split(";")[0])
            who_starts = int(server_ready.split(";")[1])

            self.audio_player.stop_music()
            self.audio_player.play_battle_music()
            self.clear_canvas()

            self.board = Board(self, self.game_box, opponent, who_starts)
            if who_starts == 1:
                self.title = Label(self.game_box, text="Your turn", font=("Calibra", 26, "bold"))
            else:
                self.title = Label(self.game_box, text=opponent.current_name + "'s turn", font=("Calibra", 26, "bold"))
            self.title.pack(pady=10)
            self.board.draw_board()

        self.clear_canvas()
        self.title = Label(self.game_box, text="Waiting for more players...", font=("Calibra", 20, "bold"))
        self.title.pack(pady=140)

        self.game_box.after(2000, ui_done)

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
