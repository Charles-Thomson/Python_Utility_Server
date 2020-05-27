
# ****
# Imports
# ****

import kivy
from kivy.app import App
from kivymd.app import MDApp
from Network import Utility_Client as Client


# ****
# Kivy Imports
# ****
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# the first page of the app, (enter the users name page)
class login_page(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_username(self, username_field):
        username = username_field
        Client.send_user_name(username)


class Utility_App(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):

        # Start the screen manager
        self.screen_manager = ScreenManager()

        # Load the first page
        self.login_page = login_page()
        screen = Screen(name="login_page")
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


# Run the application if this file is run
if __name__ == "__main__":
    Utility_App().run()
