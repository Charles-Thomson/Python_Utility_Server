Start: 12/11/2019

Application to test threading and multi-user support.

Leverages Kivy for the GUI.

Utility server allowing clients to access a number of sub-utilities:

UTILITIES

Hangman:
- Implemented from a separate project.
- Basic Hangman game.

Polish Notation Calculator:
- Implemented from a separate project.
- Allows for processing of Polish (suffix) notation equations.

Chat Room:
- Allows connected clients to "chat."
- New messages are pased to all listeing CLients
- No Local message storage

NETWORK

Client: 
- Light weight client
- Connects to server via open socket
- Passes all data via a standared encoded format
- Listens for server responce

Server: 
- Handles new client connection, passing new connection onto a open thread
- Connects user to selected util via tag in message
