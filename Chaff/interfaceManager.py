import kivy
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class InterfaceManager(BoxLayout):

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.first = Button(text="First")
        self.first.bind(on_press=self.show_second)

        self.second = Button(text="Second")
        self.second.bind(on_press=self.show_final)

        self.final = Label(text="Hello World")
        self.add_widget(self.first)

    def show_second(self, button):
        self.clear_widgets()
        self.add_widget(self.second)

    def show_final(self, button):
        self.clear_widgets()
        self.add_widget(self.final)


class MyApp(App):
    def build(self):
        return InterfaceManager(orientation='vertical')

if __name__ == '__main__':
    MyApp().run()