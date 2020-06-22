# ****
# Imports
# ****

from Utility import Message_Tags as TAG

# ****
# Const
# ****

FORMAT = 'utf-8'  # The msg encode as

clients = []
current_chat = []


# Add the new client to the clients list
def new_client(connection, user_name):
    if (connection, user_name) in clients:
        print("Client already connected")
    else:  # Check to see if the client is already connected to the chat server
        clients.append(tuple((connection, user_name)))
        print(f'\n[SYSTEM]{user_name} has connected. Connection : {connection}')
        get_connected_users(connection)  # Update the connected users with the new connected users list


# Return the connected clients
def get_connected_users(connection):
    return_clients = ""
    for client_socket in clients:
        return_clients += client_socket[1] + "\\"  # Add an element to be split on in the client
    print(return_clients)
    return_clients = TAG.GET_CONNECTED_USERS_TAG + return_clients
    bytes_msg = return_clients.encode()
    print("Sending connected users")
    for client_socket in clients:  # Send the new list of connected users to all connected users
        client_socket = client_socket[0]
        client_socket.send(bytes_msg)


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
    msg = TAG.CHAT_ROOM_TAG + user_name + "//" + msg
    for client_socket in clients:  # Send to all connected clients
        client_socket = client_socket[0]
        print(msg)
        bytes_msg = msg.encode()
        print("msg encoded")
        client_socket.send(bytes_msg)
        print("sent msg")

