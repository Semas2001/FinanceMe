from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

#set window size
Window.size = (450,750)

Window.clearcolor = 32/255, 28/255, 28/255, 1

class LoginPage(Screen):
    pass

class BP(Screen):
    def on_enter(self):
        self.files_layout = self.ids['files_layout']

    def add_file(self, file_path):
        if hasattr(self, 'files_layout'):
            new_item = BoxLayout(size_hint_y=None, height=100, padding=2, spacing=0)
            new_item.canvas.before.add(Color(0.5, 0.5, 0.5, 1))
            new_item.canvas.before.add(Rectangle(pos=new_item.pos, size=new_item.size))

            file_label = Label(text=file_path, size_hint_y=None, height=20)
            new_item.add_widget(file_label)

            self.files_layout.add_widget(new_item)
        else:
            print("Error: files_layout id is not found")

class StatisticsPage(Screen):
    pass

class AccountPage(Screen):
    pass


class ScreenManager(ScreenManager):
    pass


class FinanceMe(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        return Builder.load_file("FinanceMe.kv")

    def add_file(self, *args):
        self.file_manager.show('/')  # Start with the root directory

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        print("Selected:", path)
        self.root.get_screen('BP').add_file(path)

FinanceMe().run()
