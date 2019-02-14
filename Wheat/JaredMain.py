import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.codeinput import CodeInput
from pygments.lexers import CythonLexer

#Load kv file
Builder.load_file('dynamicEX.kv')

#First Screen
class Screen1(Screen):

    count = 0
    layouts = []

    def remove(self):
        for i in self.layouts:
            if i.children[0].active:
                self.ids.widget_list.remove_widget(i)

        self.layouts = [i for i in self.layouts if not i.children[0].active]

        if self.layouts!=[]:
            self.update_hints()
        else:
            layout = GridLayout(rows=1)
            layout.add_widget(Label(text='Nothing Here'))
            self.ids.widget_list.add_widget(layout)

    def add(self):

        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<10:
            self.count+=1
            layout = GridLayout(cols=2)
            layout.add_widget(CodeInput(lexer = CythonLexer()))
            layout.add_widget(CheckBox())
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)
            self.update_hints()
        else:
            layout = GridLayout(cols=1)
            layout.add_widget(Label(text='Only five allowed at once.\nRemove at least one to add another.'))
            button = Button(text='Acknowledge'); layout.add_widget(button)
            popup = Popup(content=layout, title='Limit Reached', size_hint=(.5,.5), auto_dismiss=False)
            button.bind(on_release=popup.dismiss)
            popup.open()

    def update_hints(self):

        for i in self.layouts:
            i.children[1].hint_text = 'Input code here'

#Initialize Screens and Start App
class MyScreenManager(ScreenManager):

    pass

#Main application
class Wheat(App):

    def build(self):
        self.sm = MyScreenManager()
        return self.sm

if __name__ == '__main__':
    Wheat().run()