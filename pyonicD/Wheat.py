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
file_dir = os.path.dirname("pyonicD")
sys.path.append(file_dir)
from pyonicD.interpreter import InterpreterGui

# file_dir = os.path.dirname("Wheat")
# sys.path.append(file_dir)

#Load kv file
Builder.load_file('Wheat.kv')

class WheatScreen(Screen):

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

        if self.layouts!=[]:
            print("nothing here")

    def add(self):

        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout = InterpreterGui()
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)