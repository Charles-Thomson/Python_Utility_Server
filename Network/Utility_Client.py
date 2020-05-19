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
SERVER = "192.168.56.1"  # Server location - robustness issue ?
ADDRESS = (SERVER, PORT)  # Address is the server IP and the PORT number being used

DISCONNECT_RESULT = "[DISCONNECT]"
DISCONNECT_MSG = "!DISCONNECT"  # For clean disconnection of client
EXIT_UTILITY = "!EXIT"
VALID_OPERATORS = " x-/+"  # Valid operators
AVAILABLE_UTILITY = ['Suffix Calculator', 'Hang Man']

# Create the client socket - socket family (Type) AF_INET - SOCK_STREAM is streaming data through the socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect client to server
client.connect(ADDRESS)


# Can change to check if the incoming msg is in a list of known error messages
# Send msg
def send(msg=''):
    # global connected
    # connected = True
    print("\n[WELCOME]  Welcome to the Python Utility Server ")
    while True:

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
            message = '[HANG_MAN_CREATION]'
            send_msg(message)
            hang_man()

        else:
            print(f'[SYSTEM] {utility_selection} is not a utility - the available utilitys are {AVAILABLE_UTILITY}')
            continue

        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing
        if DISCONNECT_RESULT in result:  # If a disconnect msg is returned
            disconnect()


# Handling the !DISCONNECT requests
def disconnect():
    print('[DISCONNECTED] You have been disconnected')
    sys.exit("\n[SYSTEM] User Disconnected")


# Handle message sending
def send_msg(message):
    if message:
        message = message.encode(FORMAT)  # Encode to bytes format
        msg_length = len(message)  # Get the length of the msg
        msg_header = str(msg_length).encode(FORMAT)  # The first msg sent(msg header), shows length of actual msg
        msg_header += b' ' * (HEADER - len(msg_header))  # Pad the msg to be len 64 (HEADER)
        # b' ' is the bytes representation of ' '
        client.send(msg_header)  # Send the msg header first
        client.send(message)  # Followed by the actual msg
    else:
        print("Can't send an empty message")


# Start and run the suffix calculator
def suffix_calculator():
    print('Welcome to the Polish Notation (Suffix) calculator')
    while True:
        message = input('Enter a suffix equation : ')

        # Check to  see if the msg is empty
        if message:
            message = '[SUFFIX_CALCULATOR]' + message  # Add a pre-message for the server
            send_msg(message)  # Need to allow the server to first create the hangman object
        else:
            continue

        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing

        if DISCONNECT_RESULT in result:  # If a disconnect msg is returned
            disconnect()

        elif '[INPUT_ERROR]' in result:  # If there is an input error msg returned
            print(f'{message} is not a valid equation')
            continue
        else:
            print(f'The result is {result}')


# Going to need to first create the object on the server
# Receive the starting message from the game
# Pass messages back to the game object and recv the update each time
def hang_man():

    result = client.recv(2048).decode(FORMAT)  # Receive the the hidden word and mxa_attempts
    result = result.split("//")  # Split the return string
    print('Welcome to Hang Man')
    print(f'The word is: {result[0]}   The maximum number of attempts is: {result[1]}')  # Print, take elements from list locations
    word = result[2]

    while True:
        message = input("\nMake a guess:   ")

        # Check to  see if the msg is empty
        if message:
            message = '[HANG_MAN]' + message  # Add a pre-message for the server
            send_msg(message)  # Need to allow the server to first create the hangman object
        else:
            continue

        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing
        if DISCONNECT_RESULT in result:  # If a disconnect msg is returned
            disconnect()
        else:
            result = result.split("//")  # Split the result - giving a list
            print(f'The word: {result[0]}  Number of failed Attempts: {result[1]}')
            if result[2] == "[GAME_WIN]":  # List element 2 is a tag - return result depending on the tag
                print(f'\n[SYSTEM - GAME_RESULT] Congratulations you won. The word is {result[0]}')
                break
            if result[2] == "[GAME_LOSE]":
                print(f'\n[SYSTEM - GAME_RESULT] You lost. The word was {word}')
                break

    send()


send()



