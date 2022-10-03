import socket
from threading import Thread
from tkinter import *


class Server:
    # Player usernames
    player_name1 = "Player1"
    player_name2 = "Player2"

    # List of connected players
    connected_players = []

    # Last decision made by player, empty after opponent is informed
    player_decision1 = ""
    player_decision2 = ""

    def __init__(self, port):
        self.port = port
        self.status_text = None
        self.status_title = None

        # Create a server window
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

        # Create the server menu
        self.draw_menu()

    def draw_menu(self):
        # Main title
        title = Label(self.serverWindow, text="CodeTTT server", font=("Calibra", 26, "bold"))

        # Status label
        self.status_title = Label(self.serverWindow, text="Status", font=("Calibra", 18, "normal"))
        self.status_text = Label(self.serverWindow, text="Starting server...", foreground="yellow", font=("Calibra", 26, "bold"))

        # Port label
        port_title = Label(self.serverWindow, text="Port", font=("Calibra", 18, "normal"))
        port_text = Label(self.serverWindow, text=self.port, font=("Calibra", 26, "bold"))

        # Placement of elements
        title.grid(row=0, column=0, padx=(150, 0), pady=(10, 0))
        self.status_title.grid(row=1, column=0, padx=(150, 0), pady=(20, 0))
        self.status_text.grid(row=2, column=0, padx=(150, 0))
        port_title.grid(row=3, column=0, padx=(150, 0), pady=(10, 0))
        port_text.grid(row=4, column=0, padx=(150, 0), pady=(10, 0))

    # Change status label text
    def change_status_text(self, text, color):
        self.status_text.config(text=text, foreground=color)

    # Start server in new thread
    def start_server(self):
        self.change_status_text("Running", "green")
        server_thread = Thread(target=self.begin_listening)
        server_thread.start()

    # Open the socket, and configure server
    def begin_listening(self):
        print("Beginning listen")
        # Get the hostname, not used for now
        host = socket.gethostname()

        server_socket = socket.socket()
        server_socket.bind(("127.0.0.1", self.port))  # Bind host address and port together

        # Configure how many client the server can listen simultaneously
        server_socket.listen(2)

        # Start listening for connections and listen for messages
        self.listen_for_messages(server_socket)

    def listen_for_messages(self, server_socket):
        conn, address = server_socket.accept()  # Accept new connection
        print("Incoming connection from: " + str(address))
        while True:
            # Receive data stream. It won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # If data is not received break
                break
            print("Message from connected user: " + str(data))

            # Split sender and command
            sender = str(data).split(":")[0]
            command = str(data).split(":")[1]

            # Determine what to do based on command sent
            if command == "MyID":  # Save the ID as a player
                print("Attemting to register player")
                self.connected_players.append(sender)
                print("A new player was registered with ID: " + sender)

                # Reply with thank u
                data = "ThankU"
                conn.send(data.encode())
            elif command == "YouReady?":  # Client is waiting for server to start the game
                data = "False"

                # If there are enough players (2), start the game, and let the first connected player be player1
                if len(self.connected_players) > 1:
                    if self.connected_players[0] == sender:
                        # We are player 1
                        data = self.player_name2 + ";1"
                    else:
                        # We are player 2
                        data = self.player_name1 + ";2"

                # Send info about opponent and who starts to the client. False if not ready
                conn.send(data.encode())
            elif command == "PleaseChoose":  # Client is waiting for opponent to make a decision
                data = "False"

                # Check if opponent made a decision
                if self.connected_players[0] == sender:
                    decision_made = self.player_decision2
                    self.player_decision2 = ""
                else:
                    decision_made = self.player_decision1
                    self.player_decision1 = ""

                # If opponent made a decision: send that, else: send false
                if len(decision_made) > 0:
                    data = decision_made
                conn.send(data.encode())
            elif command.split(";")[0] == "IChoose":  # Client informs server about selected tiles
                # Determine if it was Player1 or Player2 who just made a decision
                if self.connected_players[0] == sender:
                    print("Chosen by player 1")
                    self.player_decision1 = command.split(";")[1] + ";" + command.split(";")[2]
                else:
                    print("Chosen by player 2")
                    self.player_decision2 = command.split(";")[1] + ";" + command.split(";")[2]

                # Answer client with false
                data = "False"
                conn.send(data.encode())
            elif command.split(";")[0] == "MyUsername":  # Client is informing server about it's username
                # Save the username of the player
                if self.connected_players[0] == sender:
                    self.player_name1 = command.split(";")[1]
                else:
                    self.player_name2 = command.split(";")[1]

                # Reply with ThankU
                data = "ThankU"
                conn.send(data.encode())  # send data to the client
            else:
                # An unknown command was sent from the client
                print("----- WARNING COMMAND NOT FOUND!!!! -----:" + command)

            conn.close()  # close the connection
            break

        conn.close()  # close the connection
        self.listen_for_messages(server_socket)  # Loop back and listen for new messages/connections
