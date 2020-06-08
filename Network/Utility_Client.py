# ****
# Imports
# ****

import socket
import sys
import threading




# ****
# Const
# ****

# Header represents the max msg length, can cause issue for long msg if the header value is small
from threading import Thread

HEADER = 64  # First msg to server is always 64 - represents the length of the msg about to be received
PORT = 5060  # Port

FORMAT = 'utf-8'  # The msg encode as
SERVER = "192.168.56.1"  # Server location - robustness issue ?
ADDRESS = (SERVER, PORT)  # Address is the server IP and the PORT number being used

INPUT_ERROR_MSG = '[INPUT_ERROR]'
DISCONNECT_RESULT_MSG = "[DISCONNECT]"

DISCONNECT_MSG = "!DISCONNECT"  # For clean disconnection of client
EXIT_UTILITY_MSG = "!EXIT"

AVAILABLE_UTILITY = ['Suffix Calculator', 'Hang Man', 'Chat Room']

# Message Tags attached to messages for the server
SUFFIX_TAG = '[SUFFIX_CALCULATOR]'
HANG_MAN_TAG = '[HANG_MAN]'
CHAT_ROOM_TAG = '[CHAT_ROOM]'
EXIT_CHAT_ROOM_TAG = '[EXIT_CHAT_ROOM]'
USER_NAME_TAG = '[USER_NAME]'

RETURNED_RESULT = ""


# Create the client socket - socket family (Type) AF_INET - SOCK_STREAM is streaming data through the socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect client to server
client.connect(ADDRESS)


def send_user_name(username=""):
    print(username)
    message = USER_NAME_TAG + username
    send_msg(message)
    #utility_selection = "Suffix Calculator"
    #utility_handling(utility_selection)


# This will be called by the on button press of each navigation draw button
# Main process for client, handles selection of util
def utility_handling(utility_selection):
   #  print(f'\n[WELCOME] Hello {username} Welcome to the Python Utility Server ')
    print(f"[ACTIVE THREADS] {threading.activeCount()}")
    print("in the utility selection")
    while True:

        # utility_selection = input("\nEnter the name of the Utility you want to use or type 'help' for help:  ")
        if utility_selection == 'help':
            print(f'[HELP] The currently available utilitys are :  {AVAILABLE_UTILITY} ')
            continue

        if 'Suffix Calculator' in utility_selection:
            print("Calculator chosen")
            suffix_calculator()

        if 'Hang Man' in utility_selection:
            message = '[HANG_MAN_CREATION]'
            send_msg(message)
            hang_man()

        if 'Chat Room' in utility_selection:
            message = '[JOIN_CHAT_ROOM]'
            send_msg(message)
            # chat_room()

            thread_listen = threading.Thread(target=listen, args=())
            thread_listen.start()

            chat_room()

        if DISCONNECT_MSG in utility_selection:  # If a disconnect msg is returned
            disconnect()

        else:
            print(f'[SYSTEM] {utility_selection} is not a utility - the available utilitys are {AVAILABLE_UTILITY}')
            continue

        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing
        if DISCONNECT_RESULT_MSG in result:  # If a disconnect msg is returned
            disconnect()


# Handling the !DISCONNECT requests
def disconnect():
    print('[DISCONNECTED] You have been disconnected')
    message = DISCONNECT_MSG
    send_msg(message)
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

    return return_result()


# Check to see if play again - for hang man only currelty
def play_again_hang_man():
    replay = input("Do you want to play again? (y/n)  :   ")
    if replay == "y":
        message = '[HANG_MAN_CREATION]'
        send_msg(message)
        hang_man()
    if replay == "n":
        utility_handling()
    else:
        print(f'{replay} is not a valid choice')
        play_again_hang_man()


def return_result():
    global RETURNED_RESULT
    server_result = client.recv(2048).decode(FORMAT)
    RETURNED_RESULT = server_result
    return server_result


# Start and run the suffix calculator
def suffix_calculator():
    #print('Welcome to the Polish Notation (Suffix) calculator')
    while True:
        message = input('Enter a suffix equation : ')  # <-- Change her for refactoring

        # Check to  see if the msg is empty
        if message:
            message = SUFFIX_TAG + message  # Add a pre-message for the server
            send_msg(message)  # Need to allow the server to first create the hangman object
        else:
            continue

        result = return_result()  # can change to use the fix length header thing


        if DISCONNECT_RESULT_MSG in result:  # If a disconnect msg is returned
            disconnect()

        elif EXIT_UTILITY_MSG in result:
            print('\n[SYSTEM] Exiting Utility')
            utility_handling()

        elif INPUT_ERROR_MSG in result:  # If there is an input error msg returned
            print(f'{message} is not a valid equation')
            continue
        else:
            pass
            #print(f'The result is {result}')


# Hang man game
def hang_man():
    result = client.recv(2048).decode(FORMAT)  # Receive the the hidden word and mxa_attempts
    result = result.split("//")  # Split the return string
    print('Welcome to Hang Man')
    print(
        f'The word is: {result[0]}   The maximum number of attempts is: {result[1]}')  # Print, take elements from list locations
    word = result[2]

    while True:
        message = input("\nMake a guess:   ")

        # Check to  see if the msg is empty
        if message:
            message = HANG_MAN_TAG + message  # Add a pre-message for the server
            send_msg(message)  # Need to allow the server to first create the hangman object
        else:
            continue

        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing

        if DISCONNECT_RESULT_MSG in result:  # If a disconnect msg is returned
            disconnect()

        elif EXIT_UTILITY_MSG in result:
            print('\n[SYSTEM] Exiting Utility')
            break

        else:
            result = result.split("//")  # Split the result - giving a list
            print(f'The word: {result[0]}  Number of failed Attempts: {result[1]}')

            if result[2] == "[GAME_WIN]":  # List element 2 is a tag - return result depending on the tag
                print(f'\n[SYSTEM - GAME_RESULT] Congratulations you won. The word is {result[0]}')
                play_again_hang_man()

            if result[2] == "[GAME_LOSE]":
                print(f'\n[SYSTEM - GAME_RESULT] You lost. The word was {word}')
                play_again_hang_man()

    utility_handling()


# Create a thread to start listening
def start_listening():

    print("[SYSTEM] in Start Listening ")
    thread = threading.Thread(target=listen, args=())
    thread.start()


# This is in it's own thread
def listen():

    print("[SYSTEM] listen thread running")
    while True:
        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing

        if EXIT_UTILITY_MSG in result:
            print('\n[SYSTEM] Exiting Utility')
            sys.exit("[CLOSE_CHAT_THREAD]")  # Closes the thread

        else:
            print(f'{result}')


def chat_room():

    print("\n[CLIENT] welcome to the chat room")

    while True:
        message = input()

        if message:
            message = CHAT_ROOM_TAG + message  # Add a pre-message for the server
            send_msg(message)  # Need to allow the server to first create the hangman object
            if EXIT_UTILITY_MSG in message:
                message = EXIT_CHAT_ROOM_TAG
                send_msg(message)
                print('\n[SYSTEM-CHAT_ROOM] Exiting Utility')
                break

        else:
            continue

    utility_handling()


if __name__ == "__main__":
    username = input("Enter Username: ")
    send_user_name(username)
