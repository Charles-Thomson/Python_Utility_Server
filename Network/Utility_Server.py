# ****
# Imports
# ****

import socket
import threading
from Utility import Run_Utility as Run
from Utility import Chat_Room
import sys

sys.path.insert(1, 'PycharmProjects/Python_Utility_Server/Utility/Polish_Notation')

sys.path.insert(1, 'PycharmProjects/Python_Utility_Server/Utility/Hang_Man_Game')

# ****
# Const
# ***
# Header represents the max msg length, can cause issue for long msg if the header value is small
HEADER = 64  # First msg to server is always 64 - represents the length of the msg about to be received
PORT = 5060  # Port

# SERVER = "192.168.1.7"  # Server location
SERVER = socket.gethostbyname(socket.gethostname())  # Get the ip of this device to host the server
ADDRESS = (SERVER, PORT)  # Address is the server IP and the PORT number being used
FORMAT = 'utf-8'  # The msg encode as

DISCONNECT_MSG = "!DISCONNECT"  # For clean disconnection of client
EXIT_UTILITY_MSG = "!EXIT"  # Exit out of current utility

# Create the server socket - socket family (Type) AF_INET - SOCK_STREAM is streaming data through the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to ADDRESS
server.bind(ADDRESS)

# The available chat room objects
CHAT_ROOMS = []
CONNECTED_USERS = []


# Handle each client in new thread
def handle_client(connection, address):
    # Print when new connection is made
    print(f"[NEW_SERVER_CONNECTION] {address} connected ")
    print("in handle_client  ")

    while True:

        msg_length = connection.recv(HEADER).decode(FORMAT)  # Blocking until msg received from client -
        # The length of the message is equal to the header value
        # Decode by FORMAT as each msg is encoded

        if msg_length:  # Check if the msg has content - first msg is always blank on connection
            msg_length = int(msg_length)  # convert to int
            msg = connection.recv(msg_length).decode(FORMAT)  # The actual msg is of length msg_length(decoded HEADER)

            if '[USER_NAME]' in msg:  # If the DISCONNECT_MSG is received
                msg = msg.replace('[USER_NAME]', '')
                print(f'[SERVER] {msg} has connected ')
                connected_user = (msg, address)
                CONNECTED_USERS.append(connected_user)
                user_name = msg
                result = user_name
                print(f'[SYSTEM_CONNECTED] The connected users are {CONNECTED_USERS}')
                return_msg(connection, result,  msg)

            # If the disconnect msg is received
            if DISCONNECT_MSG in msg:  # If the DISCONNECT_MSG is received
                print(f'[DISCONNECT] {address} has disconnected')
                result = '[DISCONNECT]'
                return_msg(connection, result,  msg)
                break

            if EXIT_UTILITY_MSG in msg:
                print(f'\n[EXIT_UTILITY] {address} has exited the current utility')
                result = EXIT_UTILITY_MSG
                return_msg(connection, result, msg)
                continue

            if '[HANG_MAN_CREATION]' in msg:
                hang_man_obj = Run.create_hang_man_object()
                result = Run.initial_hang_man_details(hang_man_obj)  # Get the details for the start of the game
                return_msg(connection, result, msg)  # Pass info to the return msg function

            if '[JOIN_CHAT_ROOM]' in msg:
                Chat_Room.new_client(connection)
                result = "You have joined the chat room"
                return_msg(connection, result, msg)

            if '[CHAT_ROOM_CREATION]' in msg:
                chat_room_object = Run.create_chat_room_object()
                result = Run.initial_hang_man_details(chat_room_object)
                return_msg(connection, result, msg)
                return

            if '[SUFFIX_CALCULATOR]' in msg:
                result = Run.run_suffix_calculator(msg)  # Result of the calculator
                return_msg(connection, result, msg)  # Pass info to the return msg function

            if '[HANG_MAN]' in msg:
                result = Run.run_hang_man(msg, hang_man_obj)  # pass the msg and the game object
                return_msg(connection, result, msg)  # Pass info to the return msg function

            if '[CHAT_ROOM]' in msg:
                Chat_Room.handle_new_message(msg, connection)

            if '[EXIT_CHAT_ROOM]' in msg:
                Chat_Room.disconnect_client(connection)

    connection.close()  # Close the connection
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


def return_msg(connection, result,  msg):
    print(f'[RETURNING RESULT] Returning result :  {msg}   =   {result}')
    bytes_result = result.encode(FORMAT)  # Encode result in FORMAT
    connection.send(bytes_result)  # Send response to the client in the thread


# Server to start listening and pass new connections
def start():
    server.listen()  # Start listening
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        # This is blocking - will wait for new connection -
        # Store socket object (connection) that will allow for the return of data
        # Store the address (address) of the new connection
        thread = threading.Thread(target=handle_client,
                                  args=(connection, address))  # Pass the connection to be handled on a new thread
        # "target" is the def on the new thread - "args" are the arguments passed ot the target def
        thread.start()  # Start the new thread
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        # Print the number of active clients by number of threads
        # - 1 as the server takes a thread


print("[STARTING] server is starting")
start()
