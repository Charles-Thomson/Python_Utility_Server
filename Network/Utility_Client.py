# ****
# Imports
# ****

import socket
import sys
from string import digits
# ****
# Const
# ****

# Header represents the max msg length, can cause issue for long msg if the header value is small
HEADER = 64  # First msg to server is always 64 - represents the length of the msg about to be received
PORT = 5060  # Port
FORMAT = 'utf-8'  # The msg encode as
DISCONNECT_MSG = "!DISCONNECT"  # For clean disconnection of client
SERVER = "192.168.56.1"  # Server location - robustness issue ?
ADDRESS = (SERVER, PORT)  # Address is the server IP and the PORT number being used
VALID_OPERATORS = " x-/+"  # Valid operators


# Create the client socket - socket family (Type) AF_INET - SOCK_STREAM is streaming data through the socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect client to server
client.connect(ADDRESS)


# Can change to check if the incoming msg is in a list of known error messages
# Send msg
def send(msg):
    connected = True
    while connected:
        print("\nEnter polish notation equation:  ")
        msg = input()
        message = msg.encode(FORMAT)  # Encode to bytes format
        msg_length = len(message)  # Get the length of the msg
        msg_header = str(msg_length).encode(FORMAT)  # The first msg sent(msg header), shows length of actual msg
        msg_header += b' ' * (HEADER - len(msg_header))  # Pad the msg to be len 64 (HEADER)
        # b' ' is the bytes representation of ' '
        client.send(msg_header)  # Send the msg header first
        client.send(message)  # Followed by the actual msg
        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing
        if '[DISCONNECT]' in result:  # If a disconnect msg is returned
            print('[DISCONNECTED] You have been disconnected')
            connected = False
            break
        if '[INPUT_ERROR]' in result:  # If there is an input error msg returned
            print(f'{msg} is not a valid equation')
            continue

        print(f'The result of  {msg}  is  {result}')  # Print the result


msg = ' '
send(msg)



