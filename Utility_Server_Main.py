# ****
# Imports
# ****

import kivy

from kivy import Config
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemeManager, ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.navigationdrawer import NavigationLayout

from Network import Utility_Client


Config.set('graphics', 'multisamples', '0')

from kivy.app import App
from kivymd.app import MDApp
from Network import Utility_Client as Client, Utility_Client

# ****
# Kivy Imports
# ****
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from Utility import Message_Tags as TAG

kivy.require('1.11.1')


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    # Called when the button is pressed - work out the selection assignment
    def utility_button_selection(self, selection):
        Utility_Client.utility_handling(selection)


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Utility_App(MDApp):
    user_name_server_result = StringProperty()
    suffix_calculator_server_result = StringProperty()
    hang_man_server_result = StringProperty()
    chat_room_server_result = StringProperty()
    connected_users_server_result = StringProperty()

    user_name = user_name_server_result

    suffix_calculator_result_text = suffix_calculator_server_result  # set the result text in the suffix calculator
    hang_man_result_text = hang_man_server_result
    chat_room_result_text = chat_room_server_result
    connected_users_result_text = connected_users_server_result



    def build(self):
        pass

    def on_start(self):
        pass

    def send_username(self, username_field):
        if username_field:
            msg = username_field
            message = TAG.USER_NAME_TAG + msg
            print(message)
            Client.send_msg(message)


        else:
            print("Enter a user name")

    # Create the hang man game object
    def create_hang_man(self):
        message = TAG.HANG_MAN_CREATION_TAG
        Client.send_msg(message)
        print("[CLIENT] Hang man started")  # debug

    # Call the method in client to start a new listening thread
    def call_start_listening(self):
        Client.start_listening(self.incoming_message_Handling)

    # send message to join the chat room
    def join_chat_room(self):
        message = TAG.JOIN_CHAT_ROOM_TAG
        Client.send_msg(message)

    # ***** MESSAGE PASSING *****

    def pass_suffix_msg(self, suffix_calculator_input_field):
        msg = suffix_calculator_input_field
        message = TAG.SUFFIX_TAG + msg
        print(message)
        Client.send_msg(message)

    # Pass the input to the hang man game object
    def pass_hang_man_msg(self, hang_man_input_field):
        msg = hang_man_input_field
        message = TAG.HANG_MAN_TAG + msg
        print(message)  # Debug
        Client.send_msg(message)

    # Send a new message
    def pass_chat_room_msg(self, chat_room_input_field):
        msg = chat_room_input_field
        message = TAG.CHAT_ROOM_TAG + msg
        print(f'[PASS_CHAT_MSG] : {message}')
        Client.send_msg(message)

    # ****** Label Updates *****

    # Update the Suffix label
    def Update_Suffix_Calculator(self, result):
        print(result)
        printed_result = "The result :  " + result
        self.suffix_calculator_server_result += printed_result

    # Update the Hangman label
    def Update_Hang_Man(self, result):
        result = result.split("//")
        printed_result = "\nThe word :   " + result[0] + "  number of failed attempts  " + result[1]

        if result[2] == '[GAME_WIN]':
            printed_result = "\nCongratulations you won. The word is :  " + result[0]
        if result[2] == "[GAME_LOSE]":
            printed_result = "\nYou lost. The word is :  " + result[0]

        self.hang_man_server_result += printed_result

    # Update the chat label
    def Update_Chat(self, result):
        print(f'[UPDATE_CHAT_METHOD] {result}')
        result = result.split("//")
        printed_result = result[0] + " : " + result[1]
        print(f'[CHAT_UPDATE] Updating chat inside Utility_app with: {result}')
        printed_result = "\n" + printed_result
        self.chat_room_server_result += printed_result

    def update_connected_users(self, result):
        result = result.split("\\")
        printed_result = "The connected clients :  \n"
        for r in result:
            printed_result += r + "\n"
        self.connected_users_server_result = printed_result

    # Incoming message handling
    def incoming_message_Handling(self, result):

        if TAG.USER_NAME_TAG in result:
            result = result.replace('[USER_NAME]', '')
            self.user_name_server_result = result

        if TAG.SUFFIX_TAG in result:
            result = result.replace('[SUFFIX_CALCULATOR]', '')
            self.Update_Suffix_Calculator(result)

        if TAG.HANG_MAN_TAG in result:
            result = result.replace('[HANG_MAN]', '')
            self.Update_Hang_Man(result)

        if TAG.CHAT_ROOM_TAG in result:
            result = result.replace('[CHAT_ROOM]', '')
            self.Update_Chat(result)

        if TAG.GET_CONNECTED_USERS_TAG in result:
            result = result.replace('[GET_CONNECTED_USERS]', '')
            self.update_connected_users(result)


# Run the application if this file is run
if __name__ == "__main__":
    utility_app = Utility_App()
    utility_app.run()
