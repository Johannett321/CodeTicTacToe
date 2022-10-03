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

    # Connect to the server and send a command
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

    # Ask the opponent to choose, and inform what I choose
    def play(self, board, just_chose=None, just_won=False):
        # Inform the opponent what I choose
        if just_chose is not None:
            print("I just chose:" + str(just_chose))
            chosen_tiles = self.send_command_to_server("IChoose;" + just_chose, not just_won)
        else: # The opponent chooses first, so don't inform what i choose
            chosen_tiles = self.send_command_to_server("PleaseChoose")

        # Return if I just won, no need to wait for opponent to select
        if just_won:
            return

        def ui_loaded(tiles_chosen):
            # Wait for opponent to choose
            while tiles_chosen == "False":
                time.sleep(1)
                tiles_chosen = self.send_command_to_server("PleaseChoose")

            # Place the 'o' from the opponent
            row = int(tiles_chosen.split(";")[0])
            col = int(tiles_chosen.split(";")[1])
            board.opponent_place_o(row, col)

        # Let UI finish loading
        board.game_box.after(300, lambda: ui_loaded(chosen_tiles))

    def set_name(self, name):
        self.current_name = name
