from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from datetime import datetime

total_revenue = []
file_dates = []
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

        # Create dropdown for category selection
        category_dropdown = DropDown()

        # Customize the appearance of dropdown items
        dropdown_item_height = dp(40)  # Set dropdown item height
        dropdown_item_color = (0.2, 0.2, 0.2, 1)  # Set dropdown item color
        dropdown_item_font_size = dp(16)  # Set dropdown item font size

        if self.category == 'Income':
            categories = ['Invoice', 'Sale', 'Product']
        elif self.category == 'Outcome':
            categories = ['Invoice', 'Bills', 'Contractor', 'Other']
        for category in categories:
            btn = Button(text=category, size_hint_y=None, height=dropdown_item_height,
                         background_color=dropdown_item_color, font_size=dropdown_item_font_size)
            btn.bind(on_release=lambda btn: category_dropdown.select(btn.text))
            category_dropdown.add_widget(btn)

        category_button = Button(text='Select Category', size_hint=(None, None), size=(150, 40),
                                 background_color=(0.3, 0.3, 0.3, 1), font_size=dp(16))
        category_button.bind(on_release=category_dropdown.open)
        category_dropdown.bind(on_select=lambda instance, x: setattr(category_button, 'text', x))

        file_name_input = TextInput(hint_text="Enter file name", multiline=False)
        amount_input = TextInput(hint_text="Enter amount", multiline=False)
        confirm_button = Button(text="Confirm", size_hint_y=None, height=40, background_color=(0.1, 0.6, 0.3, 1),
                                font_size=dp(16))

        def add_file_and_amount(instance):
            selected_category = category_button.text
            self.add_file(self.file_path, file_name_input.text)
            self.add_amount(selected_category, amount_input.text)
            popup.dismiss()

        confirm_button.bind(on_press=add_file_and_amount)

        popup_content.add_widget(category_button)
        popup_content.add_widget(file_name_input)
        popup_content.add_widget(amount_input)
        popup_content.add_widget(confirm_button)

        popup = Popup(title=f"Enter {self.category} File and Amount", content=popup_content, size_hint=(None, None),
                      size=(350, 250))
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

