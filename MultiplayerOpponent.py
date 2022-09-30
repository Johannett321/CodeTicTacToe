import random
import socket
import time

from Opponent import Opponent


class MultiplayerOpponent(Opponent):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.myid = str(random.randint(0, 1000000))
        self.current_name = "Player 2"
        self.can_click = False
        self.isOnline = True

    def send_command_to_server(self, command, wait_for_answer=True):
        client_socket = socket.socket()  # instantiate
        client_socket.connect((self.ip, self.port))  # connect to the server

        client_socket.send((self.myid + ":" + command).encode())  # send message
        if wait_for_answer:
            data = client_socket.recv(1024).decode()  # receive response
            print('Received from server: ' + data)  # show in terminal
        else:
            data = None

        client_socket.close()  # close the connection
        return data

    def play(self, board, just_chose=None, just_won=False):
        if just_chose is not None:
            print("I just chose:" + str(just_chose))
            chosen_tiles = self.send_command_to_server("IChoose;" + just_chose, not just_won)
        else:
            chosen_tiles = self.send_command_to_server("PleaseChoose")

        if just_won:
            return

        while chosen_tiles == "False":
            time.sleep(1)
            chosen_tiles = self.send_command_to_server("PleaseChoose")
        row = int(chosen_tiles.split(";")[0])
        col = int(chosen_tiles.split(";")[1])
        board.opponent_place_o(row, col)

    def set_name(self, name):
        self.current_name = name
