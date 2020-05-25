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
    print(f'\n[SYSTEM] {connection} has disconnected')


# send the new message out to the other clients
def handle_new_message(msg):
    msg = msg.replace('[CHAT_ROOM]', '')
    current_chat.append(msg)
    print(f'[CURRENT_CHAT] {current_chat}')
    for client_socket in clients:
        bytes_msg = msg.encode()
        client_socket.send(bytes_msg)

