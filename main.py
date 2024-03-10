from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.config import Config

#set window size
Window.size = (450,750)

Window.clearcolor = 32/255, 28/255, 28/255, 1

class LoginPage(Screen):
    pass

class BP(Screen):
    pass

class StatisticsPage(Screen):
    pass

class AccountPage(Screen):
    pass


class ScreenManager(ScreenManager):
    pass


class FinanceMe(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("FinanceMe.kv")

FinanceMe().run()
