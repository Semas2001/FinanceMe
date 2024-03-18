from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
import os
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

#set window size
Window.size = (450,750)

Window.clearcolor = 32/255, 28/255, 28/255, 1

class LoginPage(Screen):
    pass

class BP(Screen):
    def __init__(self, **kwargs):
        super(BP, self).__init__(**kwargs)
        self.file_entries = []

    file_count = 0
    category = None
    file_path = None
    total_income = 0
    total_outcome = 0
    def on_enter(self):
        self.files_layout = self.ids['files_layout']
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)

    def show_popup(self, category):
        self.category = category
        self.file_manager.show('/')  # Start with the root directory

    def select_path(self, path):
        self.file_path = path
        self.file_manager.close()
        if self.category:
            self.popup_amount()

    def popup_amount(self):
        popup_content = BoxLayout(orientation='vertical', padding=10)
        amount_input = TextInput(hint_text="Enter amount", multiline=False)
        confirm_button = Button(text="Confirm", size_hint_y=None, height=40)

        def add_file_and_amount(instance):
            self.add_file(self.file_path)
            self.add_amount(self.category, amount_input.text)
            popup.dismiss()

        confirm_button.bind(on_press=add_file_and_amount)

        popup_content.add_widget(amount_input)
        popup_content.add_widget(confirm_button)

        popup = Popup(title=f"Enter {self.category} Amount", content=popup_content, size_hint=(None, None),
                      size=(300, 200))
        popup.open()

    def add_file(self, file_path):
        if hasattr(self, 'files_layout'):
            # Increment file count
            self.file_count += 1

            # Get current date and time
            now = datetime.now()
            formatted_date = now.strftime("%Y-%m-%d")

            file_name = os.path.basename(file_path)

            # Create a horizontal layout for the new file entry
            new_item = BoxLayout(size_hint_y=None, height=40, padding=5, spacing=5)

            # Create labels for file number, name, and date
            file_number_label = Label(text=str(self.file_count), size_hint_x=0.1)
            file_name_label = Label(text=file_name, size_hint_x=None, width=200, halign="left", text_size=(None, None))
            date_label = Label(text=formatted_date, size_hint_x=0.3, halign="right")

            # Add labels to the horizontal layout
            new_item.add_widget(file_number_label)
            new_item.add_widget(file_name_label)
            new_item.add_widget(date_label)

            # Add the new file entry to the layout
            self.files_layout.add_widget(new_item)

            # Save the file entry for reference when adding amount
            self.file_entries.append(new_item)
        else:
            print("Error: files_layout id is not found")

    def add_amount(self, category, amount):
        if hasattr(self, 'file_entries'):
            # Find the index of the last added file entry
            last_file_index = len(self.file_entries) - 1
            file_entry = self.file_entries[last_file_index]

            # Create a label for the amount
            amount_label = Label(text=f"{category}: {amount}", size_hint_x=0.3, halign="right")
            if category == 'Income':
                amount_label.color = (0, 1, 0, 1)  # Green color for income
            elif category == 'Outcome':
                amount_label.color = (1, 0, 0, 1)  # Red color for outcome

            # Add the amount label to the file entry layout
            file_entry.add_widget(amount_label)
        else:
            print("Error: file_entries not initialized")

    def exit_manager(self, *args):
        self.file_manager.close()

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
