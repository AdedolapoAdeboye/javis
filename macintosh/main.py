from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

KV = '''
<RootWidget>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0.56, 0.27, 0.68, 1  # Violet color
            Rectangle:
                pos: self.pos
                size: self.size
        
        ScrollView:
            size_hint: 1, 0.85
            pos_hint: {'x': 0, 'y': 0.15}
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
            pos_hint: {'x': 0.1, 'y': 0.05}
            hint_text: 'Enter task'
            background_color: 1, 1, 1, 1  # White background for text input
            foreground_color: 0, 0, 0, 1  # Black text color
        
        Button:
            text: '+'
            size_hint: None, None
            size: '56dp', '56dp'
            pos_hint: {'x': 0.8, 'y': 0.05}
            background_color: 0.93, 0.33, 0.36, 1  # Floating button color
            on_release: app.add_task()
'''

class RootWidget(BoxLayout):
    pass

class Javis(App):
    def build(self):
        self.title = "Javis"
        Builder.load_string(KV)
        return RootWidget()

    def add_task(self):
        task_input = self.root.ids.task_input
        task_list = self.root.ids.task_list
        task_text = task_input.text
        if task_text:
            task_item = Label(text=task_text, size_hint_y=None, height='48dp', color=(1, 1, 1, 1))  # White text color
            task_list.add_widget(task_item)
            task_input.text = ''

if __name__ == '__main__':
    Javis().run()
