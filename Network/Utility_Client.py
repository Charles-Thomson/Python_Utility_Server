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
AVAILABLE_UTILITY = ['Suffix Calculator', 'Hang Man']


# Can change to check if the incoming msg is in a list of known error messages
# Send msg
def send(msg):
    global connected
    connected = True
    print("[WELCOME]  Welcome to the Python Utility Server ")
    while connected:

        utility_selection = input("\nEnter the name of the Utility you want to use or type 'help' for help:  ")
        if utility_selection == 'help':
            print(f'[HELP] The currently available utilitys are :  {AVAILABLE_UTILITY} ')
            continue

        if 'Suffix Calculator' in utility_selection:
            print("Calculator chosen")
            message = '[SUFFIX_CALCULATOR]'
            # send_msg(message)
            suffix_calculator()

        if 'Hang Man' in utility_selection:
            print("Hang Man chosen")
            message = '[HANG_MAN]'
            send_msg(message)
            hang_man()

        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing
        if '[DISCONNECT]' in result:  # If a disconnect msg is returned
            print('[DISCONNECTED] You have been disconnected')
            connected = False
            break
        if '[INPUT_ERROR]' in result:  # If there is an input error msg returned
            print(f'{msg} is not a valid equation')
            continue

# Handle message sending
def send_msg(message):
    message = message.encode(FORMAT)  # Encode to bytes format
    msg_length = len(message)  # Get the length of the msg
    msg_header = str(msg_length).encode(FORMAT)  # The first msg sent(msg header), shows length of actual msg
    msg_header += b' ' * (HEADER - len(msg_header))  # Pad the msg to be len 64 (HEADER)
    # b' ' is the bytes representation of ' '
    client.send(msg_header)  # Send the msg header first
    client.send(message)  # Followed by the actual msg


# Currently working
def suffix_calculator():
    print('Welcome to the Polish Notation (Suffix) calculator')
    while connected:
        message = input('Enter a suffix equation : ')
        message = '[SUFFIX_CALCULATOR]' + message
        send_msg(message)

        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing
        print(f'The result is {result}')


# Going to need to first create the object on the server
# Receive the starting message from the game
# Pass messages back to the game object and recv the update each time
def hang_man():
    print('Welcome to Hang Man')

    message = '[HANG_MAN]'
    send_msg(message)  # Need to allow the server to first create the hangman object

    while connected:
        print("[HANG_MAN_RECV]")
        result = client.recv(2048).decode(FORMAT)  # Receive the start of the game (welcome msg, hidden_word ... ect )
        print(f'The result is {result}')

        # message = input('Start Guessing: ')
        # message = message + '[HANGMAN]'
        # send_msg(message)





msg = ' '
send(msg)



