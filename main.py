from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy_garden.graph import Graph, MeshLinePlot



# Set window size
Window.size = (450, 750)
Window.clearcolor = 32/255, 28/255, 28/255, 1

class LoginPage(Screen):
    pass

class BP(Screen):
    def __init__(self, **kwargs):
        super(BP, self).__init__(**kwargs)
        self.file_entries = []
        self.income_data = []
        self.outcome_data = []
        self.total_income = 0
        self.total_outcome = 0

    file_count = 0
    category = None
    file_path = None

    def on_enter(self):
        self.files_layout = self.ids['files_layout']
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)

    def show_popup(self, category):
        self.category = category
        self.file_manager.show('/')

    def select_path(self, path):
        self.file_path = path
        self.file_manager.close()
        if self.category:
            self.popup_file_and_amount()

    def popup_file_and_amount(self):
        popup_content = BoxLayout(orientation='vertical', padding=10)
        file_name_input = TextInput(hint_text="Enter file name", multiline=False)
        amount_input = TextInput(hint_text="Enter amount", multiline=False)
        confirm_button = Button(text="Confirm", size_hint_y=None, height=40)

        def add_file_and_amount(instance):
            self.add_file(self.file_path, file_name_input.text)
            self.add_amount(self.category, amount_input.text)
            popup.dismiss()

        confirm_button.bind(on_press=add_file_and_amount)

        popup_content.add_widget(file_name_input)
        popup_content.add_widget(amount_input)
        popup_content.add_widget(confirm_button)

        popup = Popup(title=f"Enter {self.category} File and Amount", content=popup_content, size_hint=(None, None),
                      size=(300, 250))
        popup.open()

    def add_file(self, file_path, file_name):
        if hasattr(self, 'files_layout'):
            # Increment file count
            self.file_count += 1
            now = datetime.now()
            formatted_datetime = now.strftime("%Y-%m-%d")
            new_item = BoxLayout(size_hint_y=None, height=40, padding=5, spacing=5)
            file_number_label = Label(text=str(self.file_count), size_hint_x=0.1)
            file_name_label = Label(text=file_name, size_hint_x=None, width=200, halign="left", text_size=(None, None))
            date_label = Label(text=formatted_datetime, size_hint_x=0.3, halign="right")
            new_item.add_widget(file_number_label)
            new_item.add_widget(file_name_label)
            new_item.add_widget(date_label)
            self.files_layout.add_widget(new_item)
            self.file_entries.append(new_item)
        else:
            print("Error: files_layout id is not found")

    def add_amount(self, category, amount):
        if hasattr(self, 'file_entries'):
            last_file_index = len(self.file_entries) - 1
            file_entry = self.file_entries[last_file_index]
            amount_label = Label(text=f"   £{amount}", size_hint_x=0.3, halign="right")
            if category == 'Income':
                amount_label.color = (0, 1, 0, 1)
                self.income_data.append(float(amount))
                self.total_income += float(amount)
            elif category == 'Outcome':
                amount_label.color = (1, 0, 0, 1)
                self.outcome_data.append(float(amount))
                self.total_outcome += float(amount)
            now = datetime.now()
            file_entry.add_widget(amount_label)
            total_revenue = self.total_income - self.total_outcome
            print(f"Total Revenue: £{total_revenue}")
            self.manager.get_screen('SP').update_total_revenue(total_revenue)
            now = datetime.now()
            formatted_datetime = now.strftime("%Y-%m-%d")
            self.manager.get_screen('SP').update_graph(total_revenue, formatted_datetime)
        else:
            print("Error: file_entries not initialized")

    def exit_manager(self, *args):
        self.file_manager.close()

class StatisticsPage(Screen):
    def __init__(self, **kwargs):
        super(StatisticsPage, self).__init__(**kwargs)
        self.graph = None  # Initialize graph as None

    def on_enter(self):
        # Access ids dictionary after the widget tree is initialized
        if self.ids.graph:
            self.graph = self.ids.graph  # Assign graph to ids.graph
            if not self.graph.plots:  # If no plots are already added to the graph
                self.initialize_graph()  # Call method to initialize graph

    def initialize_graph(self):
        # Initialize the graph and other widgets
        if self.graph:
            self.plot = MeshLinePlot(color=[1, 0, 0, 1])
            self.graph.add_plot(self.plot)
            self.total_revenue_label = Label(halign='center', valign='middle', font_size=24)
            self.add_widget(self.total_revenue_label)

    def update_graph(self, total_revenue, formatted_datetime):
        if self.plot:
            # Update the graph
            formatted_date = datetime.strptime(formatted_datetime, "%Y-%m-%d").toordinal()
            self.plot.points.append((formatted_date, total_revenue))
            self.plot.points.sort(key=lambda x: x[0])
            self.graph.x_ticks_major = len(self.plot.points)
            self.graph.x_ticks = [x[0] for x in self.plot.points]
            self.total_revenue_label.text = f"Total Revenue: £{total_revenue}"




    def update_total_revenue(self, total_revenue):
        if self.total_revenue_label:
            # Update the total revenue label
            self.total_revenue_label.text = f"Total Revenue: £{total_revenue}"
            if self.graph:
                self.graph.ymax = total_revenue + 100

class AccountPage(Screen):
    pass

class ScreenManager(ScreenManager):
    def update_statistics_page(self, total_revenue):
        statistics_page = self.get_screen('SP')
        statistics_page.update_total_revenue(total_revenue)

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
