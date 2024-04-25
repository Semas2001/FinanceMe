from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.graphics import RoundedRectangle
from kivy.uix.textinput import TextInput


def popup_file_and_amount(self):
    popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)

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

    # Customize text input appearance with rounded corners and transparency
    file_name_input.background_color = (0, 0, 0, 0)  # Set background color to transparent
    file_name_input.background_normal = ''
    file_name_input.color = (0.5, 0.5, 0.5, 1)  # Remove default background
    file_name_input.background_active = ''  # Remove active state background
    file_name_input.canvas.before.add(
        RoundedRectangle(pos=file_name_input.pos, size=file_name_input.size, radius=[10, 10, 10, 10]))

    amount_input.background_color = (0, 0, 0, 0)  # Set background color to transparent
    amount_input.background_normal = ''  # Remove default background
    amount_input.background_active = ''
    amount_input.color = (0.5, 0.5, 0.5, 1)  # Remove active state background
    amount_input.canvas.before.add(
        RoundedRectangle(pos=amount_input.pos, size=amount_input.size, radius=[10, 10, 10, 10]))

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

    # Create the popup with customized attributes
    popup = Popup(title=f"Enter {self.category} File and Amount", content=popup_content, size_hint=(None, None),
                  size=(350, 250))

    # Customize the appearance of the popup window with rounded corners
    popup.background_color = (0.2, 0.2, 0.2, 1)  # Background color
    popup.separator_color = (1, 1, 1, 1)  # Separator color
    popup.title_color = (1, 1, 1, 1)  # Title text color
    popup.title_size = dp(18)  # Title font size
    popup.content.canvas.before.add(
        RoundedRectangle(pos=popup.content.pos, size=popup.content.size, radius=[10, 10, 10, 10]))

    # Open the popup
    popup.open()