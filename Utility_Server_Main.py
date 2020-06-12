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




# ****
# TAGS
# ****

SUFFIX_TAG = '[SUFFIX_CALCULATOR]'
HANG_MAN_TAG = '[HANG_MAN]'
HANG_MAN_CREATION_TAG = '[HANG_MAN_CREATION]'
CHAT_ROOM_TAG = '[CHAT_ROOM]'
EXIT_CHAT_ROOM_TAG = '[EXIT_CHAT_ROOM]'
USER_NAME_TAG = '[USER_NAME]'
JOIN_CHAT_ROOM_TAG = '[JOIN_CHAT_ROOM]'

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

    suffix_calculator_server_result = StringProperty()
    hang_man_server_result = StringProperty()
    chat_room_server_result = StringProperty()

    user_name = StringProperty()

    suffix_calculator_result_text = suffix_calculator_server_result  # set the result text in the suffix calculator
    hang_man_result_text = hang_man_server_result
    chat_room_result_text = chat_room_server_result

    def build(self):
        pass

    def on_start(self):
        pass

    def send_username(self, username_field):
        if username_field:
            msg = username_field
            message = USER_NAME_TAG + msg
            print(message)
            result = Client.send_msg(message)
            print(result)
            self.user_name = result

        else:
            print("Enter a user name")

    def pass_suffix_msg(self, suffix_calculator_input_field):
        msg = suffix_calculator_input_field
        message = SUFFIX_TAG + msg
        print(message)
        result = Client.send_msg(message)
        print(result)
        printed_result = "\nThe result of :   " + suffix_calculator_input_field + "   =   " + result
        self.suffix_calculator_server_result += printed_result

    # Create the hang man game object
    def create_hang_man(self):
        message = HANG_MAN_CREATION_TAG

        print(message)  # debug

        result = Client.send_msg(message)

        print("[CLIENT] Hang man started")  # debug

        result = result.split("//")

        printed_result = "\nThe word :   " + result[0] + "  Maximum number of attempts:  " + result[1]

        self.hang_man_server_result += printed_result

    # Pass the input to the hang man game object
    def pass_hang_man_msg(self, hang_man_input_field):
        msg = hang_man_input_field
        message = HANG_MAN_TAG + msg

        print(message)  # Debug

        result = Client.send_msg(message)

        print(result)  # Debug

        result = result.split("//")

        printed_result = "\nThe word :   " + result[0] + "  number of failed attempts  " + result[1]

        if result[2] == '[GAME_WIN]':
            printed_result = "\nCongratulations you won. The word is :  " + result[0]

        if result[2] == "[GAME_LOSE]":
            printed_result = "\nYou lost. The word is :  " + result[0]

        self.hang_man_server_result += printed_result

    # Call the method in client to start a new listening thread
    def call_start_listening(self):
        Client.start_listening()

    # send message to join the chat room
    def join_chat_room(self):
        message = JOIN_CHAT_ROOM_TAG
        Client.send_msg(message)

    # Send a new message
    def pass_chat_room_msg(self, chat_room_input_field):
        msg = chat_room_input_field
        message = CHAT_ROOM_TAG + msg
        # self.chat_room_server_result += message
        Client.send_msg(message)

    # Update the chat label when called from the client
    def update_chat(self, result):

        print(f'[CHAT_UPDATE] Updating chat inside Utility_app with: {result}')
        print(type(result))
        self = self
        self.chat_room_result_text = result


# Run the application if this file is run
if __name__ == "__main__":
    utility_app = Utility_App()
    utility_app.run()
