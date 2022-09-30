import random
import time
import socket
from threading import Thread, main_thread
from tkinter import *


class Server:
    player_name1 = "Player1"
    player_name2 = "Player2"
    connected_players = []
    player_decision1 = ""
    player_decision2 = ""

    def __init__(self, port):
        self.port = port
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
        port_title = Label(self.serverWindow, text="Port", font=("Calibra", 18, "normal"))
        port_text = Label(self.serverWindow, text=self.port, font=("Calibra", 26, "bold"))

        title.grid(row=0, column=0, padx=(150, 0), pady=(10, 0))
        self.status_title.grid(row=1, column=0, padx=(150, 0), pady=(20, 0))
        self.status_text.grid(row=2, column=0, padx=(150, 0))
        port_title.grid(row=3, column=0, padx=(150, 0), pady=(10, 0))
        port_text.grid(row=4, column=0, padx=(150, 0), pady=(10, 0))

    def change_status_text(self, text, color):
        self.status_text.config(text=text, foreground=color)

    def start_server(self):
        self.change_status_text("Running", "green")
        server_thread = Thread(target=self.begin_listening)
        server_thread.start()

    def begin_listening(self):
        print("Beginning listen")
        # get the hostname
        host = socket.gethostname()

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind(("127.0.0.1", self.port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        server_socket.listen(2)

        self.listen_for_messages(server_socket)

    def listen_for_messages(self, server_socket):
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            print("from connected user: " + str(data))
            sender = str(data).split(":")[0]
            command = str(data).split(":")[1]
            if command == "MyID":
                print("Attemting to register player")
                self.connected_players.append(sender)
                data = "ThankU"
                print("ID REGISTERED")
                conn.send(data.encode())
            elif command == "YouReady?":
                print("Connected users: " + str(self.connected_players) + " amount: " + str(len(self.connected_players)))
                data = "False"
                if len(self.connected_players) > 1:
                    if self.connected_players[0] == sender:
                        # We are player 1
                        data = self.player_name2 + ";1"
                    else:
                        # We are player 2
                        data = self.player_name1 + ";2"
                conn.send(data.encode())  # send data to the client
            elif command == "PleaseChoose":
                data = "False"
                if self.connected_players[0] == sender:
                    decision_made = self.player_decision2
                    self.player_decision2 = ""
                else:
                    decision_made = self.player_decision1
                    self.player_decision1 = ""
                if len(decision_made) > 0:
                    data = decision_made
                conn.send(data.encode())  # send data to the client
            elif command.split(";")[0] == "IChoose":
                if self.connected_players[0] == sender:
                    print("Chosen by player 1")
                    self.player_decision1 = command.split(";")[1] + ";" + command.split(";")[2]
                else:
                    print("Chosen by player 2")
                    self.player_decision2 = command.split(";")[1] + ";" + command.split(";")[2]
                data = "False"
                conn.send(data.encode())  # send data to the client
            elif command.split(";")[0] == "MyUsername":
                if self.connected_players[0] == sender:
                    print("Chosen by player 1: ")
                    self.player_name1 = command.split(";")[1]
                else:
                    print("Chosen by player 2")
                    self.player_name2 = command.split(";")[1]
                data = "ThankU"
                conn.send(data.encode())  # send data to the client
            else:
                print("----- WARNING COMMAND NOT FOUND!!!! -----:" + command)
            conn.close()  # close the connection
            break

        conn.close()  # close the connection
        self.listen_for_messages(server_socket)
