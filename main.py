from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy_garden.graph import Graph, MeshLinePlot
from datetime import timedelta
import random

total_revenue = []
file_dates = []
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

    def show_popup(self, category):
        self.category = category
        self.popup_file_manager()

    def popup_file_manager(self):
        from kivymd.uix.filemanager import MDFileManager
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
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
            file_dates.append(formatted_datetime)  # Store file addition date
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
            phtotal_revenue = self.total_income - self.total_outcome
            total_revenue.append(phtotal_revenue)
            print(f"Total Revenue: £{phtotal_revenue}")
            file_entry.add_widget(amount_label)
        else:
            print("Error: file_entries not initialized")

    def exit_manager(self, *args):
        self.file_manager.close()


class StatisticsPage(Screen):
    def __init__(self, **kwargs):
        super(StatisticsPage, self).__init__(**kwargs)
        self.total_revenue = total_revenue
        self.prediction_plots = []

    def on_enter(self):
        self.update_graph()

    def update_graph(self):
        if not self.total_revenue or not file_dates:
            return

        graph = self.ids.graph
        graph.clear_widgets()

        # Adjusting the size of the graph
        graph.size_hint = (0.9, 5.5)  # Adjust these values as needed

        ymax = max(self.total_revenue) + 100
        graph_obj = Graph(xlabel='Date', ylabel='Total Revenue', x_ticks_minor=5,
                          x_ticks_major=1, y_ticks_major=int(ymax / 10), y_grid_label=True,
                          x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                          xmin=0, xmax=len(file_dates), ymin=0, ymax=ymax)
        dates = [datetime.strptime(date, "%Y-%m-%d") for date in file_dates]
        x_labels = {i: date.strftime("%Y-%m-%d") for i, date in enumerate(dates)}
        graph.x_ticks_major = 1
        graph.x_labels = x_labels
        for i in range(1, len(self.total_revenue)):
            plot = MeshLinePlot()
            plot.points = [(i - 1, self.total_revenue[i - 1]), (i, self.total_revenue[i])]
            if self.total_revenue[i] > self.total_revenue[i - 1]:
                plot.color = (0, 1, 0, 1)
            else:
                plot.color = (1, 0, 0, 1)
            graph_obj.add_plot(plot)
        graph.add_widget(graph_obj)


    def generate_prediction_data(self):
        last_index = len(self.total_revenue) - 1
        if last_index >= 0:
            last_date = datetime.strptime(file_dates[last_index], "%Y-%m-%d")
            next_date_1 = last_date + timedelta(days=1)
            next_date_2 = last_date + timedelta(days=2)
            new_revenue_1 = self.total_revenue[last_index] + random.uniform(-50, 50)  # Adjust range for diversity
            new_revenue_2 = new_revenue_1 + random.uniform(-50, 50)  # Adjust range for diversity
            file_dates.append(next_date_1.strftime("%Y-%m-%d"))
            self.total_revenue.append(new_revenue_1)

            file_dates.append(next_date_2.strftime("%Y-%m-%d"))
            self.total_revenue.append(new_revenue_2)

            self.update_graph()
class AccountPage(Screen):
    pass

class ScreenManager(ScreenManager):
    def add_file(self, *args):
        super().add_file(*args)
        self.get_screen('BP').update_statistics_page()

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
