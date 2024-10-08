# ****
# Imports
# ****

import socket
import sys
import threading

from nltk.lm.vocabulary import _

from Utility import Message_Tags as TAG




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

AVAILABLE_UTILITY = ['Suffix Calculator', 'Hang Man', 'Chat Room']

RETURNED_RESULT = ""


# Create the client socket - socket family (Type) AF_INET - SOCK_STREAM is streaming data through the socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect client to server
client.connect(ADDRESS)


def send_user_name(username=""):
    print(username)
    message = TAG.USER_NAME_TAG + username
    send_msg(message)


# Handling the !DISCONNECT requests
def disconnect():
    print('[DISCONNECTED] You have been disconnected')
    message = TAG.DISCONNECT_MSG
    send_msg(message)
    sys.exit("\n[SYSTEM] User Disconnected")


# Handle message sending
def send_msg(message):
    if message:
        print(f'[CLIENT_SEND_MSG] : {message}')
        message = message.encode(FORMAT)  # Encode to bytes format
        msg_length = len(message)  # Get the length of the msg
        msg_header = str(msg_length).encode(FORMAT)  # The first msg sent(msg header), shows length of actual msg
        msg_header += b' ' * (HEADER - len(msg_header))  # Pad the msg to be len 64 (HEADER)
        # b' ' is the bytes representation of ' '
        client.send(msg_header)  # Send the msg header first
        client.send(message)  # Followed by the actual msg
    else:
        print("Can't send an empty message")


def return_result():
    global RETURNED_RESULT
    server_result = client.recv(2048).decode(FORMAT)
    RETURNED_RESULT = server_result
    return server_result


# Create a thread to start listening
def start_listening(incoming_message_callback):
    print("[SYSTEM] in Start Listening ")
    thread = threading.Thread(target=listen, args=(incoming_message_callback, _), daemon=True)
    thread.start()


# This is in it's own thread
def listen(incoming_message_callback, _):

    print("[SYSTEM] listen thread running")
    while True:
        result = client.recv(2048).decode(FORMAT)  # can change to use the fix length header thing
        print(f'[CLIENT_MSG] message received from the server is: {result}')
        incoming_message_callback(result)


if __name__ == "__main__":
    pass

