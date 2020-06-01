
# ****
# Imports
# ****

import kivy

from kivy import Config
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemeManager
from kivymd.uix.navigationdrawer import NavigationLayout

Config.set('graphics', 'multisamples', '0')

from kivy.app import App
from kivymd.app import MDApp
from Network import Utility_Client as Client


# ****
# Kivy Imports
# ****
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


kivy.require('1.11.1')


class Navigation_Test(NavigationLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class Header_Bar(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Header_Action_Bar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# the first page of the app, (enter the users name page)
class login_page(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_username(self, username_field):
        username = username_field
        # Client.send_user_name(username)

    def next_page(self):
        utility_app.screen_manager.current = 'home_page'


# Home pae of the UI
class home_page(NavigationLayout):
    pass


class Utility_App(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"

        self.screen_manager = ScreenManager()

    def build(self):
        self.theme_cls.primary_palette = "Blue"

        # Start the screen manager

        # login page
        self.login_page = login_page()
        screen = Screen(name="login_page")
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)


        # home page
        self.home_page = home_page()
        screen = Screen(name="home_page")
        screen.add_widget(self.home_page)
        self.screen_manager.add_widget(screen)

        # Return the screen manager
        return self.screen_manager


# Run the application if this file is run
if __name__ == "__main__":
    utility_app = Utility_App()
    utility_app.run()
