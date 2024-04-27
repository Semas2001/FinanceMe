from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.lang import Builder
from kivymd.app import MDApp
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from Screens.bp import BP
from Screens.loginPage import LoginPage
from Screens.statistics import StatisticsPage
from Screens.accountPage import AccountPage


total_revenue = []
file_dates = []
# Set window size
Window.size = (450, 750)
Window.clearcolor = 32/255, 28/255, 28/255, 1


class FinanceMe(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_file("FinanceMe.kv")
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginPage(name='LP'))
        screen_manager.add_widget(BP(name='BP'))
        screen_manager.add_widget(StatisticsPage(name='SP'))
        screen_manager.add_widget(AccountPage(name='AP'))
        return screen_manager
    def add_file(self, *args):
        self.file_manager.show('/')
    def exit_manager(self, *args):
        self.file_manager.close()
    def select_path(self, path):
        print("Selected:", path)
        self.root.get_screen('BP').add_file(path)

FinanceMe().run()
