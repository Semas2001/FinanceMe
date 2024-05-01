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
import openpyxl


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
        popup_content = BoxLayout(orientation='vertical', padding=15, spacing=15)

        type_dropdown = DropDown()
        dropdown_item_height = dp(40)
        dropdown_item_color = (0.2, 0.2, 0.2, 1)
        dropdown_item_font_size = dp(16)

        if self.category == 'Income':
            categories = ['Invoice', 'Sale', 'Product']
        elif self.category == 'Outcome':
            categories = ['Invoice', 'Bills', 'Contractor', 'Other']
        for category in categories:
            btn = Button(text=category, size_hint_y=None, height=dropdown_item_height,
                         background_color=dropdown_item_color, font_size=dropdown_item_font_size)
            btn.bind(on_release=lambda btn: type_dropdown.select(btn.text))
            type_dropdown.add_widget(btn)

        type_button = Button(text='Select Type', size_hint=(None, None), size=(150, 40),
                             background_color=(0.3, 0.3, 0.3, 1), font_size=dp(16))
        type_button.bind(on_release=type_dropdown.open)
        type_dropdown.bind(on_select=lambda instance, x: setattr(type_button, 'text', x))

        file_name_input = TextInput(hint_text="Enter file name", multiline=False)
        amount_input = TextInput(hint_text="Enter amount", multiline=False)
        confirm_button = Button(text="Confirm", size_hint_y=None, height=40, background_color=(0.1, 0.6, 0.3, 1),
                                font_size=dp(16))

        def add_file_and_amount(instance):
            selected_type = type_button.text
            selected_category = type_button.text
            amount = amount_input.text.strip()
            if not amount:
                self.show_error_popup("Amount is required. Please enter an amount.")
                return
            try:
                float_amount = float(amount)
            except ValueError:
                self.show_error_popup("Incorrect amount. Please enter a valid number.")
                return
            self.add_file(self.file_path, file_name_input.text, selected_category)
            self.add_amount(selected_type, float_amount)
            popup.dismiss()

        confirm_button.bind(on_press=add_file_and_amount)

        type_button.pos_hint = {'center_x': 0.5}

        popup_content.add_widget(file_name_input)
        popup_content.add_widget(amount_input)
        popup_content.add_widget(type_button)
        popup_content.add_widget(confirm_button)

        popup = Popup(title=f"{self.category}", content=popup_content, size_hint=(None, None),
                      size=(250, 300))
        popup.open()

    def add_file(self, file_path, file_name, category):
        if hasattr(self, 'files_layout'):
            self.file_count += 1
            now = datetime.now()
            formatted_datetime = now.strftime("%Y-%m-%d")
            file_dates.append(formatted_datetime)  # Store file addition date
            new_item = BoxLayout(size_hint_y=None, height=40, padding=5, spacing=5)
            file_number_label = Label(text=str(self.file_count), size_hint_x=0.05)
            file_name_label = Label(text=file_name, size_hint_x=0.3, width=200, halign="left", text_size=(None, None))
            category_label = Label(text=category, size_hint_x=0.5, halign="center")
            date_label = Label(text=formatted_datetime, size_hint_x=0.7, halign="right")
            new_item.add_widget(file_number_label)
            new_item.add_widget(category_label)
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
            if self.category == 'Income':
                amount_label.color = (0, 1, 0, 1)
                self.income_data.append(float(amount))
                self.total_income += float(amount)
            elif self.category == 'Outcome':
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

    def show_error_popup(self, message):
        error_label = Label(text=message, halign='center', size_hint=(None, None), size=(300, 100))
        error_popup = Popup(title='Error', content=error_label, size_hint=(None, None), size=(300, 150))
        error_popup.open()

    def show_filter_popup(self):
        popup_content = BoxLayout(orientation='vertical', padding=15, spacing=15)

        type_dropdown = Spinner(text='Choose Type',
                                values=['All', 'Invoice', 'Sale', 'Product', 'Bills', 'Contractor', 'Other'])
        category_dropdown = Spinner(text='Choose Category', values=['All', 'Income', 'Outcome'])
        filter_button = Button(text="Apply Filter", size_hint_y=None, height=40, background_color=(0.1, 0.6, 0.3, 1),
                               font_size=dp(16))

        def apply_filter(instance):
            selected_type = type_dropdown.text if type_dropdown.text != 'All' else None
            selected_category = category_dropdown.text if category_dropdown.text != 'All' else None
            self.filter_entries(selected_type, selected_category)
            popup.dismiss()

        filter_button.bind(on_press=apply_filter)

        popup_content.add_widget(type_dropdown)
        popup_content.add_widget(category_dropdown)
        popup_content.add_widget(filter_button)

        popup = Popup(title="Filter Files", content=popup_content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def filter_entries(self, selected_type, selected_category):
        if hasattr(self, 'file_entries'):
            for entry in self.file_entries:
                entry_visible = True
                entry_category = entry.children[1].text
                if selected_category and selected_category != 'All' and entry_category != selected_category:
                    entry_visible = False
                if selected_type and selected_type != 'All' and entry.children[2].text.split('   £')[
                    0] != selected_type:
                    entry_visible = False
                if entry_visible:
                    entry.opacity = 1
                    entry.height = dp(40)
                else:
                    entry.opacity = 0
                    entry.height = 0
        else:
            print("Error: file_entries not initialized")

    def show_invoice_popup(self):
        popup_content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        spinner = Spinner(text='Select Type', values=['Input', 'Output'])
        popup_content.add_widget(spinner)

        client_name_input = TextInput(hint_text="Client Name", multiline=False, size_hint_y=None, height=dp(40))
        popup_content.add_widget(Label(text="Client Name:"))
        popup_content.add_widget(client_name_input)
        item_input = TextInput(hint_text="Item/Service", multiline=False, size_hint_y=None, height=dp(40))
        quantity_input = TextInput(hint_text="Quantity", multiline=False, input_type='number', size_hint_y=None,
                                   height=dp(40))
        price_input = TextInput(hint_text="Price", multiline=False, input_type='number', size_hint_y=None,
                                height=dp(40))
        add_item_button = Button(text="Add Item", size_hint_y=None, height=dp(40),
                                 background_color=(0.1, 0.6, 0.3, 1), font_size=dp(16))

        item_layout = BoxLayout(orientation='vertical', spacing=10)

        popup_content.add_widget(Label(text="Items/Services:"))
        popup_content.add_widget(item_input)
        popup_content.add_widget(quantity_input)
        popup_content.add_widget(price_input)
        popup_content.add_widget(add_item_button)

        total_price_label = Label(text="Total Price: £0.00", size_hint_y=None, height=dp(40))
        popup_content.add_widget(total_price_label)

        def add_item(instance):
            item = item_input.text.strip()
            quantity = quantity_input.text.strip()
            price = price_input.text.strip()

            if not all([item, quantity, price]):
                show_error_popup("Item, Quantity, and Price are required.")
                return

            try:
                quantity = int(quantity)
                price = float(price)
            except ValueError:
                show_error_popup("Quantity and Price must be numbers.")
                return

            item_label = Label(text=f"{item} (x{quantity}): £{price * quantity:.2f}")
            item_layout.add_widget(item_label)

            item_input.text = ""
            quantity_input.text = ""
            price_input.text = ""
            total_price = sum(float(child.text.split(': £')[1]) for child in item_layout.children)
            total_price_label.text = f"Total Price: £{total_price:.2f}"

        add_item_button.bind(on_release=add_item)
        popup_content.add_widget(item_layout)

        generate_button = Button(text="Generate Invoice", size_hint_y=None, height=dp(40),
                                 background_color=(0.1, 0.6, 0.3, 1), font_size=dp(16))

        def generate_invoice(instance):
            client_name = client_name_input.text.strip()
            invoice_type = spinner.text.strip()

            if not client_name or item_layout.children == []:
                show_error_popup("Client Name and at least one item are required.")
                return

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Item", "Quantity", "Price"])
            total_price = 0
            for child in item_layout.children:
                item_text = child.text.split('(')[0].strip()
                quantity_text = child.text.split('x')[1].split(')')[0].strip()
                price_text = child.text.split('£')[1].strip()
                ws.append([item_text, quantity_text, price_text])
                total_price += float(price_text)
            ws.append(["Total Price", "", total_price])
            ws.append(["Invoice Type", "", invoice_type])
            wb.save(f"Invoice_{client_name}.xlsx")
            wb.close()

            popup.dismiss()

        generate_button.bind(on_release=generate_invoice)
        popup_content.add_widget(generate_button)

        popup = Popup(title="Invoice Generation", content=popup_content, size_hint=(None, None), size=(400, 600))
        popup.open()

def show_error_popup(message):
    error_popup = Popup(title='Error', content=Label(text=message, halign='center'),
                        size_hint=(None, None), size=(300, 150))
    error_popup.open()