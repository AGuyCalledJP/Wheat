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
import menu

import sys
import os
from os.path import abspath, join, dirname
file_dir = os.path.dirname("Wheat")
sys.path.append(file_dir)
from Wheat.interpreter import InterpreterGui
from Wheat.FunctionPlotter import FunctionPlotter
from Wheat.draw import Draw
from Wheat.Calculator import Calculator
from Wheat.Geometry import Geometry
from kivy.storage.jsonstore import JsonStore

store = JsonStore('children.json')

#Load kv file
Builder.load_file('home.kv')

class DrawLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(DrawLayout, self).__init__(**kwargs)

class WheatScreen(Screen):

    count = 1
    layouts = []
    currentKeys = []
    d = 1
    draw = ObjectProperty()
    widg = ObjectProperty()
    sStr = 'child'

    def remove(self):
        rem = 0
        getLost = []
        it = 0
        for i in self.layouts:
            main = i
            contained = i.children[0].ids.check
            if contained.active:
                rem = rem + 1
                self.ids.widget_list.remove_widget(main)
                getLost.append(it)
            it = it + 1
        self.count = self.count - rem
        print(len(self.layouts))
        print(len(getLost))
        for i in getLost:
            del self.layouts[i]

    def add(self):
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<10:
            self.count = self.count + 1
            layout = FloatLayout(size_hint=(None,None), size = self.size)
            print(layout.size)
            layout.add_widget(InterpreterGui())
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def addFunc(self):
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout =  FloatLayout(size_hint=(None,None), size = self.size)
            layout.add_widget(FunctionPlotter());
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def addCalc(self):
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout =  FloatLayout(size_hint=(None,None), size = self.size)
            layout.add_widget(Calculator());
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def addGeo(self):
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout =  FloatLayout(size_hint=(None,None), size = self.size)
            layout.add_widget(Geometry());
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def drawToggle(self):
        if self.d == 1:
            self.draw.disabled = True
            # self.widg.disabled = False
            self.d = 0
        else:
            self.draw.disabled = False
            # self.widg.disabled = True
            self.d = 1

    def Save(self):
        self.currentKeys = []
        if len(self.layouts) > 0:
            it = 0
            for i in self.layouts:
                saveMe = str(self.sStr) + str(it)
                local = i.children[0].pos
                widgType = ''
                a = i.children[0].ids
                if 'calc' in a:
                    widgType = 'calc'
                elif 'func' in a:
                    widgType = 'func'
                elif 'geo' in a:
                    widgType = 'geo'
                elif 'interp' in a:
                    widgType = 'interp'
                it = it + 1
                self.currentKeys.append(saveMe)
                store.put(saveMe, location=local, wType = widgType)
                print(store.exists(saveMe))

    def Load(self):
        print("hello there")
        print(len(self.currentKeys))
        if len(self.currentKeys) > 0:
            for curr in self.currentKeys:
                elem = store.get(curr)
                print(elem)
                print(type(elem))
                loc = elem['location']
                wt = elem['wType']
                if 'calc' in wt:
                    self.addCalcAux(loc)
                elif 'func' in wt:
                    self.addFuncAux(loc)
                elif 'geo' in wt:
                    self.addGeoAux(loc)
                elif 'interp' in wt:
                    self.addAux(loc)

    def addAux(self, pos):
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<10:
            self.count = self.count + 1
            layout = FloatLayout(size_hint=(None,None), size = self.size)
            print(layout.size)
            layout.add_widget(InterpreterGui(pos=pos))
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def addFuncAux(self,pos):
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout = FloatLayout(size_hint=(None,None), size = self.size)
            layout.add_widget(FunctionPlotter(pos=pos));
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def addCalcAux(self,pos):
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout = FloatLayout(size_hint=(None,None), size = self.size)
            layout.add_widget(Calculator(pos=pos));
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def addGeoAux(self,pos):
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout = FloatLayout(size_hint=(None,None), size = self.size)
            layout.add_widget(Geometry(pos=pos));
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    #Incorporationg writing functionality
    def clear(self):
        self.ids.pad.ids.paintWid.clear_canvas()

    def undo(self):
        self.ids.pad.ids.paintWid.undo()
    def redo(self):
        self.ids.pad.ids.paintWid.redo()





#-------------------------------- Identical Copy of Above---------------

class WheatScreen2(Screen):

    count = 1
    layouts = []
    d = 1
    draw = ObjectProperty()

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
        print(self.size)
        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout = FloatLayout(size_hint=(None,None), size = self.size)
            print(layout.size)
            layout.add_widget(InterpreterGui())
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def addFunc(self):

        if self.layouts==[]:
            self.ids.widget_list.clear_widgets()

        if len(self.ids.widget_list.children)<4:
            layout = FloatLayout(size_hint=(None,None))
            layout.add_widget(FunctionPlotter());
            self.count += 1
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)

    def drawToggle(self):
        if self.d == 1:
            self.draw.disabled = True
            self.d = 0
        else:
            self.draw.disabled = False
            self.d = 1

class WheatBlocksDropDownMenu(menu.MenuDropDown):
    pass

class WheatBlocksDropDownMenuButton(menu.MenuButton):
    dropdown_cls = ObjectProperty(WheatBlocksDropDownMenu)

class DrawDropDownMenu(menu.MenuDropDown):
    pass

class DrawDropDownMenuButton(menu.MenuButton):
    dropdown_cls = ObjectProperty(DrawDropDownMenu)
