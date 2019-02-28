from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.uix.codeinput import CodeInput
from kivy.uix.checkbox import CheckBox
from pygments.lexers import CythonLexer
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.switch import Switch
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (ObjectProperty, NumericProperty,
                             OptionProperty, BooleanProperty,
                             StringProperty, ListProperty)
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from time import time
import traceback


import sys
import os
from os.path import abspath, join, dirname
file_dir = os.path.dirname("pyonic")
sys.path.append(file_dir)

file_dir = os.path.dirname("Wheat")
sys.path.append(file_dir)
from pyonic.interpreterwrapper import InterpreterWrapper
from pyonic.jediinterface import get_completions, get_defs
from pyonic.widgets import ColouredButton
from WheatBlock2 import WheatBlock

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
            layout = WheatBlock2()
            self.count += 1
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
            main = i
            contained = i.children[0].children[0].children
            for i in contained:
                if i.id == "check":
                    if i.active:
                        self.ids.widget_list.remove_widget(main)
        #     if i.children[0].active:
        #         self.ids.widget_list.remove_widget(i)

        # self.layouts = [i for i in self.layouts if not i.children[0].active]

        if self.layouts!=[]:
            print("nothing here")
            # self.update_hints()
        else:
            layout = GridLayout(rows=1)
            layout.add_widget(Label(text='Nothing Here'))
            self.ids.widget_list.add_widget(layout)

    def add(self):

        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout = WheatBlock()
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)
            # self.update_hints()
        # else:
        #     layout = GridLayout(cols=1)
        #     layout.add_widget(Label(text='Only five allowed at once.\nRemove at least one to add another.'))
        #     button = Button(text='Acknowledge'); layout.add_widget(button)
        #     popup = Popup(content=layout, title='Limit Reached', size_hint=(.5,.5), auto_dismiss=False)
        #     button.bind(on_release=popup.dismiss)
        #     popup.open()

    # def update_hints(self):

    #     for i in self.layouts:
    #         i.children[1].hint_text = 'Input code here'

#Initialize Screens and Start App
class MyScreenManager(ScreenManager):

    pass

#Main application
class Wheat(App):
    subprocesses = []

    ctypes_working = BooleanProperty(True)

    manager = ObjectProperty()

    # Properties relating to settings in the Settings screen
    setting__throttle_output = BooleanProperty()
    setting__throttle_output_default = True
    setting__show_input_buttons = BooleanProperty()
    setting__show_input_buttons_default = True
    setting__autocompletion = BooleanProperty()
    setting__autocompletion_default = True
    setting__autocompletion_brackets = BooleanProperty()
    setting__autocompletion_brackets_default = True
    setting__text_input_height = NumericProperty()
    setting__text_input_height_default = 3
    setting__rotation = StringProperty()
    setting__rotation_default = 'portrait'

    def build(self):
        self.sm = MyScreenManager()
        return self.sm

if __name__ == '__main__':
    Wheat().run()