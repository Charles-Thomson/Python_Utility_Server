
# ****
# Imports
# ****

import kivy

from kivy import Config
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemeManager, ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
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


class Header_Bar(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Header_Action_Bar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# the first page of the app, (enter the users name page)
class login_page(BoxLayout):
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


class ContentNavigationDrawer(BoxLayout):
    pass


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

    def build(self):
        pass

    def on_start(self):
        icons_item = {
            "folder": "Help",
            "account-multiple": "Chat Room",
            "star": "Hang Man",
            "history": "Suffix Calculator",
            "checkbox-marked": "Shared with me",
            "upload": "Upload",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )


# Run the application if this file is run
if __name__ == "__main__":
    utility_app = Utility_App()
    utility_app.run()
