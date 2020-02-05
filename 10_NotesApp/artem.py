from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class List(Screen):
    pass


class Editor(Screen):
    pass


class Note(Button):
    pass


class NotesApp(App):
    screen_manager = ScreenManager()

    def build(self):
        self.list = List()
        self.editor = Editor()
        self.screen_manager.add_widget(self.list)
        self.screen_manager.add_widget(self.editor)

        return self.screen_manager

    def edit_a_note(self, text):
        self.editor.ids.text_input.text = text

    def save_a_note(self, text):
        self.list.ids.notes.add_widget(Note(text=text))


if __name__ == '__main__':
    from kivy.core.window import Window
    from kivy.utils import get_color_from_hex
    Window.clearcolor = get_color_from_hex('#fff4d9')
    NotesApp().run()
