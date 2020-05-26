# ****
# Imports
# ****


# ****
# Const
# ****

FORMAT = 'utf-8'  # The msg encode as

clients = []
current_chat = []


# Add the new client to the clients list
def new_client(connection):
    clients.append(connection)
    print(f'\n[SYSTEM]{connection} has connected')


# Disconnect a client from the chat room
def disconnect_client(connection):
    clients.remove(connection)
    print(f'\n[SYSTEM_CHAT_DISCONNECT] {connection} has disconnected')


# send the new message out to the other clients
def handle_new_message(msg, connection, user_name):
    msg = msg.replace('[CHAT_ROOM]', '')  # Strip the tag
    current_chat.append(msg)  # Debug
    print(f'[CURRENT_CHAT] {current_chat}')
    user = connection  # The senders connection
    msg = user_name + ": " + msg  # Add the senders username to the returning msg
    for client_socket in clients:
        if client_socket != user:
            bytes_msg = msg.encode()
            client_socket.send(bytes_msg)

