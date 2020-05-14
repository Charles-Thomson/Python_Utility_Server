# ****
# Imports
# ****

import socket
import threading

from Utility.Polish_Notation import Polish_Notation_Calculator as Polish_Notation

import sys

sys.path.insert(1, 'PycharmProjects/Python_Utility_Server/Utility/Polish_Notation')

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
VALID_OPERATORS = " x-/+"  # Valid operators


# Create the server socket - socket family (Type) AF_INET - SOCK_STREAM is streaming data through the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to ADDRESS
server.bind(ADDRESS)


# Handle each client in new thread
def handle_client(connection, address):
    # Print when new connection is made
    print(f"[NEW CONNECTION] {address} connected ")

    connected = True  # While the client is connected
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)  # Blocking until msg received from client -
        # The length of the message is equal to the header value
        # Decode by FORMAT as each msg is encoded
        if msg_length:  # Check if the msg has content - first msg is always blank on connection
            msg_length = int(msg_length)  # convert to int
            msg = connection.recv(msg_length).decode(FORMAT)  # The actual msg is of length msg_length(decoded HEADER)
            if msg == DISCONNECT_MSG:  # If the DISCONNECT_MSG is received
                print(f'[DISCONNECT] {address} has disconnected')
                result = '[DISCONNECT]'
                return_msg(connection, result,  msg)
                connected = False  # or "break - breaks out of the loop on disconnect request
                break

            # check_input_validity(connection, msg)  # Check the validity of the msg

            print(f"[{address}] has sent {msg}")  # Print the msg and the address it came from

            user_input = msg  # Name change for consistency in computation module

            computation_obj = Polish_Notation.start_computation(user_input)  # Make a new computation object and pass the user_input

            print(computation_obj.global_result)

            result = str(computation_obj.global_result)  # result pulled from a global var in the computation object and converted to string to allow for encoding

            print(f'Result in the server is:  {result}')  # Debug print

            return_msg(connection, result, msg)  # Pass info to the return msg function

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
