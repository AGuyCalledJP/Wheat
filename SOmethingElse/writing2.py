import kivy

from kivy.graphics import Line, Color, InstructionGroup
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

from kivy.graphics import Color, Ellipse, Line, Rectangle

Builder.load_file('writing2.kv')

class PaintWidget(Widget):
    undolist = []
    objects = []
    drawing = False

    def on_touch_up(self, touch):
        self.drawing = False

    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.drawing:
                self.points.append(touch.pos)
                self.obj.children[-1].points = self.points
            else:
                self.drawing = True
                self.points = [touch.pos]
                self.obj = InstructionGroup()
                self.obj.add(Color(0,0,0))
                self.obj.add(Line(width = 2.5))
                self.objects.append(self.obj)
                self.canvas.add(self.obj)


    def undo(self):
        item = self.objects.pop(-1)
        self.undolist.append(item)
        self.canvas.remove(item)

    def redo(self):
        item = self.undolist.pop(-1)
        self.objects.append(item)
        self.canvas.add(item)

    def clear_canvas(self):
        print("Clearing")
        self.objects = []
        self.canvas.clear()

class PaintScreen(Screen):
    pass

class Manager(ScreenManager):
    pass

class Clear(Button):
    pass

class PaintApp(App):
    def build(self):
        self.sm = Manager()
        self.sm.PaintScreen = PaintScreen()
#        self.sm.PaintScreen.PaintWidget = PaintWidget()
#        self.painter = self.sm.PaintScreen.PaintWidget;
#        self.sm.PaintScreen.add_widget(Clear())
        return self.sm

if __name__ == '__main__':
    PaintApp().run()
