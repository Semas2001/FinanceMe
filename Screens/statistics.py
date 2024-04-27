from kivy.uix.screenmanager import Screen
from kivy_garden.graph import Graph, MeshLinePlot
from datetime import datetime
from kivy.properties import BooleanProperty
from FinanceMe.AI import generate_prediction, delete_generated_data
from .bp import total_revenue,file_dates
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.label import Label



class StatisticsPage(Screen):
    prediction_active = BooleanProperty(False)
    graph_initialized = False

    def __init__(self,**kwargs):
        super(StatisticsPage, self).__init__(**kwargs)
        self.total_revenue = total_revenue
        self.file_dates = file_dates
        self.prediction_active = False
        self.prediction_plots = []

    def on_enter(self):
        if not self.files_exist():
            self.show_no_data_popup()
        elif not self.graph_initialized:
            self.update_graph()
            self.graph_initialized = True
        else:
            self.update_graph()

    def on_leave(self):
        if self.prediction_active:
            self.toggle_prediction(False)

    def files_exist(self):
        return len(file_dates) > 0

    def update_graph(self):
        if not self.total_revenue or not file_dates:
            return

        graph = self.ids.graph
        graph.clear_widgets()
        graph.size_hint = (0.9, 5.5)

        ymax = max(self.total_revenue) + 100
        ymax = float(ymax)
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

    def delete_generated_data(total_revenue, file_dates):
        del total_revenue[-2:]
        del file_dates[-2:]

        return total_revenue, file_dates
    def toggle_prediction(self, active):
        global file_dates
        self.prediction_active = active
        if active:
            self.generate_prediction_data()
            self.update_graph()
            self.show_data_hint(True)
        else:
            total_revenue, file_dates = delete_generated_data(self.total_revenue, file_dates)
            self.update_graph()
            self.show_data_hint(False)

    def generate_prediction_data(self):
        if self.prediction_active:
            generate_prediction(self.total_revenue, file_dates)
            self.update_graph()

    def show_data_hint(self, active):
        hint_label = self.ids.hint_label
        if active:
            hint_label.text = "Hint: The more data you add, the more accurate the AI prediction becomes."
            hint_label.color = (0.2, 0.5, 0.9, 1)  # Adjust color as needed
        else:
            hint_label.text = ""

    def show_no_data_popup(self):
        popup_content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        message_label = Label(text="There is no data to show.", size_hint_y=None, height=dp(40))
        redirect_button = Button(text="Go to BP page", size_hint_y=None, height=dp(40))

        def redirect_to_bp_page(instance):
            self.manager.current = "BP"  # Redirect to BP page
            popup.dismiss()

        redirect_button.bind(on_release=redirect_to_bp_page)

        popup_content.add_widget(message_label)
        popup_content.add_widget(redirect_button)

        popup = Popup(title="No Data", content=popup_content, size_hint=(None, None), size=(300, 200))
        popup.open()
