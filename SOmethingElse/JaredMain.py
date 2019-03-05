import kivy

from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.switch import Switch
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
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
from kivy.uix.floatlayout import FloatLayout
from pygments.lexers import CythonLexer
import sys
import os
from os.path import abspath, join, dirname
file_dir = os.path.dirname("Wheat")
sys.path.append(file_dir)

#Load kv file
Builder.load_file('JaredMain.kv')

#First Screen
class Screen2(Screen):
    count = 1
    layouts = []
    fPos = [{'y':0},{'y':.3},{'y':.6},{'y':.9},{'y':.8}]
    fS = [(1,.3),(1,.3),(1,.3),(1,.3),(1,.3)]
    checkBox1 = [{'x': 0, 'y': 0},{'x': 0, 'y': .3},{'x': 0, 'y': .6},{'x': 0, 'y': .9},{'x': 0, 'y': .8}]
    codeBlocks = [{'x': .15, 'y': 0},{'x': .15, 'y': .3},{'x': .15, 'y': .6},{'x': .15, 'y': .9},{'x': .15, 'y': .8}]
    checkBox2 = [{'x': .85, 'y': 0}, {'x': .85, 'y': .3}, {'x': .85, 'y': .6}, {'x': .85, 'y': .9}, {'x': .85, 'y': .8}]
    def remove(self):
        if self.count > 1:
            self.count -= 1
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

        if len(self.ids.widget_list.children)<4:
            layout = FloatLayout(pos_hint = self.fPos[self.count], size_hint = self.fS[self.count])
            widget = CodeInput(lexer = CythonLexer(),pos_hint = self.codeBlocks[self.count], size_hint = (.70,1))
            widget2 = CheckBox(pos_hint = self.checkBox1[self.count], size_hint = (.15,1))
            widget3 = CheckBox(pos_hint = self.checkBox2[self.count], size_hint = (.85,1))
            self.count += 1
            layout.add_widget(widget2)
            layout.add_widget(widget)
            layout.add_widget(widget3)
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)
            self.update_hints()
        # else:
        #     layout = GridLayout(cols=1)
        #     layout.add_widget(Label(text='Only five allowed at once.\nRemove at least one to add another.'))
        #     button = Button(text='Acknowledge'); layout.add_widget(button)
        #     popup = Popup(content=layout, title='Limit Reached', size_hint=(.5,.5), auto_dismiss=False)
        #     button.bind(on_release=popup.dismiss)
        #     popup.open()

    def update_hints(self):

        for i in self.layouts:
            i.children[1].hint_text = 'Input code here'
class Screen1(Screen):

    count = 1
    layouts = []
    fPos = [{'y':0},{'y':.3},{'y':.6},{'y':.9},{'y':.8}]
    fS = [(1,.3),(1,.3),(1,.3),(1,.3),(1,.3)]
    checkBox1 = [{'x': 0, 'y': 0},{'x': 0, 'y': .3},{'x': 0, 'y': .6},{'x': 0, 'y': .9},{'x': 0, 'y': .8}]
    codeBlocks = [{'x': .15, 'y': 0},{'x': .15, 'y': .3},{'x': .15, 'y': .6},{'x': .15, 'y': .9},{'x': .15, 'y': .8}]
    checkBox2 = [{'x': .85, 'y': 0}, {'x': .85, 'y': .3}, {'x': .85, 'y': .6}, {'x': .85, 'y': .9}, {'x': .85, 'y': .8}]
    def remove(self):
        if self.count > 1:
            self.count -= 1
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

        if len(self.ids.widget_list.children)<4:
            layout = FloatLayout(pos_hint = self.fPos[self.count], size_hint = self.fS[self.count])
            widget = CodeInput(lexer = CythonLexer(),pos_hint = self.codeBlocks[self.count], size_hint = (.70,1))
            widget2 = CheckBox(pos_hint = self.checkBox1[self.count], size_hint = (.15,1))
            widget3 = CheckBox(pos_hint = self.checkBox2[self.count], size_hint = (.85,1))
            self.count += 1
            layout.add_widget(widget2)
            layout.add_widget(widget)
            layout.add_widget(widget3)
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)
            self.update_hints()
        # else:
        #     layout = GridLayout(cols=1)
        #     layout.add_widget(Label(text='Only five allowed at once.\nRemove at least one to add another.'))
        #     button = Button(text='Acknowledge'); layout.add_widget(button)
        #     popup = Popup(content=layout, title='Limit Reached', size_hint=(.5,.5), auto_dismiss=False)
        #     button.bind(on_release=popup.dismiss)
        #     popup.open()

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
