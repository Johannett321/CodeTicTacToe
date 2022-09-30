import time
from socket import socket
from threading import Thread, main_thread
from tkinter import *


class Server:
    def __init__(self):
        self.status_text = None
        self.status_title = None

        self.serverWindow = Tk()
        self.serverWindow.resizable(width=False, height=False)
        self.serverWindow.wm_title("Server")
        self.serverWindow.pack_propagate(False)

        self.frame = Frame(self.serverWindow, width=500, height=600)
        self.frame.place(x=700, y=0)
        self.frame.pack_propagate(False)

        # Centering window
        window_width = 500
        window_height = 600
        screen_width = self.serverWindow.winfo_screenwidth()
        screen_height = self.serverWindow.winfo_screenheight()
        x_cordinate = int((screen_width / 5) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.serverWindow.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        self.draw_menu()

    def draw_menu(self):
        title = Label(self.serverWindow, text="CodeTTT server", font=("Calibra", 26, "bold"))
        self.status_title = Label(self.serverWindow, text="Status", font=("Calibra", 18, "normal"))
        self.status_text = Label(self.serverWindow, text="Starting server...", foreground="yellow", font=("Calibra", 26, "bold"))

        title.grid(row=0, column=0, padx=(150, 0), pady=(10, 0))
        self.status_title.grid(row=1, column=0, padx=(150, 0), pady=(20, 0))
        self.status_text.grid(row=2, column=0, padx=(150, 0))

    def change_status_text(self, text, color):
        self.status_text.config(text=text, foreground=color)

    def start_server(self):
        self.change_status_text("Running", "green")
        server_thread = Thread(target=self.begin_listening)
        server_thread.start()

    def begin_listening(self):
        with socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 65432))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
