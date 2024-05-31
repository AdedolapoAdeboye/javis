import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.contextmenu import ContextMenu, ContextMenuItem
from kivy.lang import Builder
from kivy.uix.filechooser import FileChooserIconView

# Initialize Firebase
cred = credentials.Certificate('path/to/your/GoogleService-Info.plist')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-project-id.appspot.com'
})
db = firestore.client()
bucket = storage.bucket()

KV = '''
<RootWidget>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: app.theme_colors[app.current_theme]['background']
            Rectangle:
                pos: self.pos
                size: self.size

        ScrollView:
            size_hint: 1, 0.65
            pos_hint: {'x': 0, 'y': 0.35}
            do_scroll_x: False
            BoxLayout:
                id: task_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

        TextInput:
            id: task_input
            size_hint: 0.8, None
            height: '48dp'
            pos_hint: {'x': 0.1, 'y': 0.25}
            hint_text: 'Enter task'
            background_color: app.theme_colors[app.current_theme]['text_input_background']
            foreground_color: app.theme_colors[app.current_theme]['text_input_foreground']

        Button:
            text: '+'
            size_hint: None, None
            size: '56dp', '56dp'
            pos_hint: {'x': 0.8, 'y': 0.25}
            background_normal: 'icons/add.png'
            on_release: app.add_task()

        Spinner:
            text: 'Theme'
            values: ['Light Mode', 'Dark Mode', 'AMOLED Dark Mode', 'Blue on White', 'Pink on White', 'Yellow on Black', 'Blue on Black']
            size_hint: 0.6, None
            height: '48dp'
            pos_hint: {'x': 0.2, 'y': 0.95}
            on_text: app.change_theme(self.text)

        Spinner:
            text: 'Security'
            values: ['None', 'PIN', 'Face ID']
            size_hint: 0.6, None
            height: '48dp'
            pos_hint: {'x': 0.2, 'y': 0.85}
            on_text: app.change_security(self.text)

        Button:
            text: 'Save to Cloud'
            size_hint: 0.6, None
            height: '48dp'
            pos_hint: {'x': 0.2, 'y': 0.15}
            on_release: app.save_to_cloud()

        Button:
            text: 'Export as PDF'
            size_hint: 0.6, None
            height: '48dp'
            pos_hint: {'x': 0.2, 'y': 0.05}
            on_release: app.export_to_pdf()
'''

class RootWidget(BoxLayout):
    pass

class ToDoApp(App):
    theme_colors = {
        'Light Mode': {
            'background': (1, 1, 1, 1),
            'text_input_background': (1, 1, 1, 1),
            'text_input_foreground': (0, 0, 0, 1),
            'button_background': (0.93, 0.33, 0.36, 1),
            'task_text': (0, 0, 0, 1),
        },
        'Dark Mode': {
            'background': (0.12, 0.12, 0.12, 1),
            'text_input_background': (0.25, 0.25, 0.25, 1),
            'text_input_foreground': (1, 1, 1, 1),
            'button_background': (0.93, 0.33, 0.36, 1),
            'task_text': (1, 1, 1, 1),
        },
        'AMOLED Dark Mode': {
            'background': (0, 0, 0, 1),
            'text_input_background': (0.1, 0.1, 0.1, 1),
            'text_input_foreground': (1, 1, 1, 1),
            'button_background': (0.93, 0.33, 0.36, 1),
            'task_text': (1, 1, 1, 1),
        },
        'Blue on White': {
            'background': (1, 1, 1, 1),
            'text_input_background': (1, 1, 1, 1),
            'text_input_foreground': (0, 0, 1, 1),
            'button_background': (0, 0, 1, 1),
            'task_text': (0, 0, 1, 1),
        },
        'Pink on White': {
            'background': (1, 1, 1, 1),
            'text_input_background': (1, 1, 1, 1),
            'text_input_foreground': (1, 0, 0.87, 1),
            'button_background': (1, 0, 0.87, 1),
            'task_text': (1, 0, 0.87, 1),
        },
        'Yellow on Black': {
            'background': (0, 0, 0, 1),
            'text_input_background': (0.1, 0.1, 0.1, 1),
            'text_input_foreground': (1, 1, 0, 1),
            'button_background': (1, 1, 0, 1),
            'task_text': (1, 1, 0, 1),
        },
        'Blue on Black': {
            'background': (0, 0, 0, 1),
            'text_input_background': (0.1, 0.1, 0.1, 1),
            'text_input_foreground': (0, 0, 1, 1),
            'button_background': (0, 0, 1, 1),
            'task_text': (0, 0, 1, 1),
        },
    }

    current_theme = 'Light Mode'
    current_security = 'None'
    pin_code = None

    def build(self):
        self.title = "Javis"
        Builder.load_string(KV)
        self.check_security()
        return RootWidget()

    def add_task(self):
        task_input = self.root.ids.task_input
        task_list = self.root.ids.task_list
        task_text = task_input.text
        if task_text:
            task_item = Label(
                text=task_text,
                size_hint_y=None,
                height='48dp',
                color=self.theme_colors[self.current_theme]['task_text']
            )
            task_item.bind(on_touch_down=self.show_context_menu)
            task_list.add_widget(task_item)
            task_input.text = ''

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.root.canvas.before.clear()
        with self.root.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(rgba=self.theme_colors[theme_name]['background'])
            Rectangle(pos=self.root.pos, size=self.root.size)
        # Update existing task items
        for child in self.root.ids.task_list.children:
            if isinstance(child, Label):
                child.color = self.theme_colors[theme_name]['task_text']
        # Update text input background and foreground
        self.root.ids.task_input.background_color = self.theme_colors[theme_name]['text_input_background']
        self.root.ids.task_input.foreground_color = self.theme_colors[theme_name]['text_input_foreground']
        # Update button background
        for child in self.root.children:
            if isinstance(child, Button) and child.text == '+':
                child.background_color = self.theme_colors[theme_name]['button_background']

    def change_security(self, security_type):
        self.current_security = security_type
        if security_type == 'PIN':
            self.set_pin_code()
        self.check_security()

    def set_pin_code(self):
        content = BoxLayout(orientation='vertical')
        pin_input = TextInput(hint_text='Set PIN', password=True, multiline=False)
        content.add_widget(pin_input)
        content.add_widget(Button(text='Set', on_release=lambda x: self.save_pin(pin_input.text)))

        popup = Popup(title='Set PIN', content=content, size_hint=(0.8, 0.4))
        popup.open()

    def save_pin(self, pin):
        self.pin_code = pin
        self.check_security()

    def check_security(self):
        if self.current_security == 'Face ID':
            self.authenticate_face_id()
        elif self.current_security == 'PIN':
            self.authenticate_pin()
        # No security does not require authentication

    def authenticate_face_id(self):
        # Simulating Face ID, real implementation would use appropriate API
        self.show_error_popup('Face ID Authentication is not supported yet.')

    def authenticate_pin(self):
        content = BoxLayout(orientation='vertical')
        pin_input = TextInput(hint_text='Enter PIN', password=True, multiline=False)
        content.add_widget(pin_input)
        content.add_widget(Button(text='Verify', on_release=lambda x: self.verify_pin(pin_input.text)))

        popup = Popup(title='Enter PIN', content=content, size_hint=(0.8, 0.4))
        popup.open()

    def verify_pin(self, pin):
        if pin == self.pin_code:
            self.root.ids.task_input.text = ''  # Clear the task input
        else:
            self.show_error_popup('Incorrect PIN')

    def show_error_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    def show_context_menu(self, instance, touch):
        if instance.collide_point(*touch.pos) and touch.is_double_tap:
            context_menu = ContextMenu()
            context_menu.add_widget(ContextMenuItem(text='Delete', icon='icons/delete.png', on_release=lambda x: self.delete_task(instance)))
            context_menu.add_widget(ContextMenuItem(text='Modify', icon='icons/edit.png', on_release=lambda x: self.modify_task(instance)))
            context_menu.add_widget(ContextMenuItem(text='Mark as Done', icon='icons/done.png', on_release=lambda x: self.mark_task_done(instance)))
            context_menu.open(touch.pos)

    def delete_task(self, task_item):
        self.root.ids.task_list.remove_widget(task_item)

    def modify_task(self, task_item):
        content = BoxLayout(orientation='vertical')
        task_input = TextInput(text=task_item.text, multiline=False)
        content.add_widget(task_input)
        content.add_widget(Button(text='Save', on_release=lambda x: self.save_modified_task(task_item, task_input.text)))

        popup = Popup(title='Modify Task', content=content, size_hint=(0.8, 0.4))
        popup.open()

    def save_modified_task(self, task_item, new_text):
        task_item.text = new_text
        self.root.ids.task_input.text = ''
        Popup.dismiss()

    def mark_task_done(self, task_item):
        task_item.color = (0, 1, 0, 1)  # Mark the task as done by changing its color to green
        task_item.text = f"[Done] {task_item.text}"

    def save_to_cloud(self):
        task_list = self.root.ids.task_list
        tasks = [child.text for child in task_list.children if isinstance(child, Label)]
        task_data = {'tasks': tasks}
        db.collection('todos').document('my_todo_list').set(task_data)
        self.show_error_popup('Tasks saved to cloud!')

    def export_to_pdf(self):
        task_list = self.root.ids.task_list
        tasks = [child.text for child in task_list.children if isinstance(child, Label)]
        
        filechooser = FileChooserIconView()
        popup = Popup(title='Select Save Location', content=filechooser, size_hint=(0.9, 0.9))
        filechooser.bind(on_submit=lambda obj, selection, touch: self.create_pdf(selection[0], tasks))
        popup.open()

    def create_pdf(self, filepath, tasks):
        pdf = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        pdf.drawString(100, height - 100, "To-Do List")

        for i, task in enumerate(tasks):
            pdf.drawString(100, height - 130 - i * 20, task)

        pdf.save()
        self.show_error_popup('Tasks exported to PDF!')

if __name__ == '__main__':
    ToDoApp().run()
