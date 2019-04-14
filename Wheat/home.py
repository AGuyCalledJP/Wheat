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
from Wheat.Tex import Tex
from kivy.storage.jsonstore import JsonStore

store = JsonStore('Wheat/Notebook/PageState/children.json')
stuff = JsonStore('Wheat/Notebook/PageState/childInfo.json')

#Load kv file
Builder.load_file('home.kv')

class DrawLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(DrawLayout, self).__init__(**kwargs)

class WheatScreen(Screen):

    layouts = []
    count = 1
    layouts2 = []
    count2 = 1
    layouts3 = []
    count3 = 1
    #currentKeys = []
    universalConstant = 3
    interp = 0
    interpLoc = []
    calc = 0
    calcLoc = []
    geo = 0
    geoLoc = []
    func = 0
    funcLoc = []
    tex = 0
    texLoc = []
    d = 1
    draw = ObjectProperty()
    manager = ObjectProperty()
    space1 = ObjectProperty()
    space2 = ObjectProperty()
    space3 = ObjectProperty()
    currSpace = 0
    numSpace = 3
    sStr = 'child'
    curr = 0

    def remove(self):
        if self.currSpace is 0:
            rem = 0
            getLost = []
            it = 0
            for i in self.layouts:
                main = i
                contained = i.children[0].ids.check
                if contained.active:
                    rem = rem + 1
                    if 'interp' in i.children[0].ids:
                        i.children[0].restart_interpreter()
                    self.space1.ids.flone.remove_widget(main)
                    getLost.append(it)
                it = it + 1
            self.count = self.count - rem
            print(len(self.layouts))
            print(len(getLost))
            for i in getLost:
                del self.layouts[i]
        elif self.currSpace is 1:
            rem = 0
            getLost = []
            it = 0
            for i in self.layouts2:
                main = i
                contained = i.children[0].ids.check
                if contained.active:
                    rem = rem + 1
                    if 'interp' in i.children[0].ids:
                        i.children[0].restart_interpreter()
                    self.space2.ids.fltwo.remove_widget(main)
                    getLost.append(it)
                it = it + 1
            self.count2 = self.count2 - rem
            print(len(self.layouts2))
            print(len(getLost))
            for i in getLost:
                del self.layouts2[i]
        else:
            rem = 0
            getLost = []
            it = 0
            for i in self.layouts3:
                main = i
                contained = i.children[0].ids.check
                if contained.active:
                    rem = rem + 1
                    if 'interp' in i.children[0].ids:
                        i.children[0].restart_interpreter()
                    self.space3.ids.flthree.remove_widget(main)
                    getLost.append(it)
                it = it + 1
            self.count3 = self.count3 - rem
            print(len(self.layouts3))
            print(len(getLost))
            for i in getLost:
                del self.layouts3[i]


    def pageForward(self):
        print("AY")
        self.curr = self.curr + 1
        print(self.currSpace)
        self.currSpace = (self.currSpace + 1) % self.numSpace
        print(self.currSpace)
        if self.currSpace is 0 and self.curr is not 0:  
            for i in self.layouts:
                print(i)
                self.space1.ids.flone.remove_widget(i)
            self.layouts = []
        elif self.currSpace is 1 and self.curr is not 1:
            for i in self.layouts2:
                print(i)
                self.space2.ids.fltwo.remove_widget(i)
            self.layouts2 = []
        elif self.currSpace is 2 and self.curr is not 2:
            for i in self.layouts3:
                print(i)
                self.space3.ids.flthree.remove_widget(i)
            self.layouts3 = []
        if self.currSpace is 0:
            self.manager.current = 'o'
        elif self.currSpace is 1:
            self.manager.current = 't'
        else:
            self.manager.current = 'tr'

    def pageBack(self):
        print("Yo")
        if self.curr > 0:
            self.curr = self.curr - 1
            print(self.currSpace)
            self.currSpace = (self.currSpace + 2) % self.numSpace
            print(self.currSpace)
            if self.currSpace is 0:
                self.manager.current = 'o'
            elif self.currSpace is 1:
                self.manager.current = 't'
            else:
                self.manager.current = 'tr'  

    def add(self):
        if self.currSpace is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()

            if self.interp < self.universalConstant:
                self.interp = self.interp + 1
                self.interpLoc.append(self.count)
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                w = InterpreterGui()
                w.restart_interpreter()
                layout.add_widget(w)
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
            else:
                rem = self.interpLoc[0]
                #probably need to add another matrix to track which layout each is in
                self.interpLoc = self.interpLoc[1:-1]
                self.interpLoc.append(self.count)
                print(self.interpLoc)
                self.space1.ids.flone.remove_widget(self.layouts[rem])
                del self.layouts[rem]
        elif self.currSpace is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()

            if self.interp < self.universalConstant:
                self.interp = self.interp + 1
                self.interpLoc.append(self.count)
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                w = InterpreterGui()
                w.restart_interpreter()
                layout.add_widget(w)
                self.count2 += 1
                self.space2.ids.fltwo.add_widget(layout)
                self.layouts2.append(layout)
            else:
                rem = self.interpLoc[0]
                self.interpLoc = self.interpLoc[1:-1]
                self.interpLoc.append(self.count)
                print(self.interpLoc)
                self.space2.ids.fltwo.remove_widget(self.layouts2[rem])
                del self.layouts2[rem]
        elif self.currSpace is 2:
            if self.layouts3==[]:
                self.space3.ids.flthree.clear_widgets()

            if self.interp < self.universalConstant:
                self.interp = self.interp + 1
                self.interpLoc.append(self.count)
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                w = InterpreterGui()
                w.restart_interpreter()
                layout.add_widget(w)
                self.count3 += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)
            else:
                rem = self.interpLoc[0]
                self.interpLoc = self.interpLoc[1:-1]
                self.interpLoc.append(self.count)
                print(self.interpLoc)
                self.space3.ids.flthree.remove_widget(self.layouts3[rem])
                del self.layouts3[rem]

    def addFunc(self):
        if self.currSpace is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()
            if self.func < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(FunctionPlotter());
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
        elif self.currSpace is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()
            if self.func < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(FunctionPlotter());
                self.count2 += 1
                self.space2.ids.fltwo.add_widget(layout)
                self.layouts2.append(layout)
        else:
            if self.layouts3==[]:
                self.space1.ids.flone.clear_widgets()
            if self.func < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(FunctionPlotter());
                self.count += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)

    def addCalc(self):
        if self.currSpace is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()

            if self.calc < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(Calculator());
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
        elif self.currSpace is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()

            if self.calc < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(Calculator());
                self.count2 += 1
                self.space2.ids.fltwo.add_widget(layout)
                self.layouts2.append(layout)
        else:
            if self.layouts3==[]:
                self.space3.ids.flthree.clear_widgets()
            if self.func < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(FunctionPlotter());
                self.count3 += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)

    def addGeo(self):
        if self.currSpace is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()

            if self.geo < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(Geometry());
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
        elif self.currSpace is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()

            if self.geo < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(Geometry());
                self.count2 += 1
                self.space2.ids.fltwo.add_widget(layout)
                self.layouts2.append(layout)
        else:
            if self.layouts3==[]:
                self.space3.ids.flthree.clear_widgets()
            if self.geo < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(Geometry());
                self.count3 += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)


    def addTex(self):
        if self.currSpace is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()

            if self.tex < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(Tex());
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
        elif self.currSpace is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()

            if self.tex < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(Tex());
                self.count2 += 1
                self.space2.ids.fltow.add_widget(layout)
                self.layouts2.append(layout)
        else:
            if self.layouts3==[]:
                self.space3.ids.flthree.clear_widgets()
            if self.tex < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size)
                layout.add_widget(Tex());
                self.count3 += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)

    def drawToggle(self):
        if self.d == 1:
            self.draw.disabled = True
            self.d = 0
        else:
            self.draw.disabled = False
            self.d = 1

    def Save(self):
        self.ids.pad.Save()
        self.currentKeys = []
        if self.curr >= 0:
            for i in self.layouts:
                it = 0
                #Save the widget itself
                saveMe = "P" + str(self.curr) + str(self.sStr) + str(it)
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
                #Save the information associated with said widget
                bundle = []
                if widgType is 'interp':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, prior = bundle[0], curr = bundle[1])
                elif widgType is 'calc':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, eq_text = bundle[0], comp_text = bundle[1])
                elif widgType is 'func':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, eq_text = bundle[0], comp_text = bundle[1])
            for i in self.layouts2:
                it = 0
                #Save the widget itself
                saveMe = "P" + str(self.curr + 1) + str(self.sStr) + str(it)
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
                #Save the information associated with said widget
                bundle = []
                if widgType is 'interp':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, prior = bundle[0], curr = bundle[1])
                elif widgType is 'calc':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, eq_text = bundle[0], comp_text = bundle[1])
                elif widgType is 'func':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, eq_text = bundle[0], comp_text = bundle[1])
            for i in self.layouts:
                it = 0
                #Save the widget itself
                saveMe = "P" + str(self.curr + 2) + str(self.sStr) + str(it)
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
                #Save the information associated with said widget
                bundle = []
                if widgType is 'interp':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, prior = bundle[0], curr = bundle[1])
                elif widgType is 'calc':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, eq_text = bundle[0], comp_text = bundle[1])
                elif widgType is 'func':
                    bundle = i.children[0].Save()
                    stuff.put(saveMe, eq_text = bundle[0], comp_text = bundle[1])

    def Load(self):
        print(store.keys())
        for curr in store.keys():
            print(curr)
            pageStr = "P" + str(self.curr)
            if pageStr in curr:
                elem = store.get(curr)
                discharged = stuff.get(curr)
                print(elem)
                print(type(elem))
                loc = elem['location']
                wt = elem['wType']
                if 'calc' in wt:
                    res = self.addCalcAux(loc,0)
                    calc = self.layouts[res-1].children[0]
                    eq_text = discharged['eq_text']
                    comp_text = discharged['comp_text']
                    calc.Load(eq_text,comp_text)
                elif 'func' in wt:
                    res = self.addFuncAux(loc,0)
                    func = self.layouts[res-1].children[0]
                    eq_text = discharged['eq_text']
                    comp_text = discharged['comp_text']
                    func.Load(eq_text,comp_text)
                elif 'geo' in wt:
                    self.addGeoAux(loc,0)
                elif 'interp' in wt:
                    res = self.addAux(loc,0)
                    interp = self.layouts[res-1].children[0]
                    prior = discharged['prior']
                    curr = discharged['curr']
                    interp.Load(prior, curr)
            pageStr2 = "P" + str(self.curr + 1)
            if pageStr2 in curr:
                elem = store.get(curr)
                discharged = stuff.get(curr)
                print(elem)
                print(type(elem))
                loc = elem['location']
                wt = elem['wType']
                if 'calc' in wt:
                    res = self.addCalcAux(loc,1)
                    calc = self.layouts2[res-1].children[0]
                    eq_text = discharged['eq_text']
                    comp_text = discharged['comp_text']
                    calc.Load(eq_text,comp_text)
                elif 'func' in wt:
                    res = self.addFuncAux(loc,1)
                    func = self.layouts2[res-1].children[0]
                    eq_text = discharged['eq_text']
                    comp_text = discharged['comp_text']
                    func.Load(eq_text,comp_text)
                elif 'geo' in wt:
                    self.addGeoAux(loc,1)
                elif 'interp' in wt:
                    res = self.addAux(loc,1)
                    interp = self.layouts2[res-1].children[0]
                    prior = discharged['prior']
                    curr = discharged['curr']
                    interp.Load(prior, curr)
            pageStr3 = "P" + str(self.curr + 2)
            if pageStr3 in curr:
                elem = store.get(curr)
                discharged = stuff.get(curr)
                print(elem)
                print(type(elem))
                loc = elem['location']
                wt = elem['wType']
                if 'calc' in wt:
                    res = self.addCalcAux(loc,2)
                    calc = self.layouts3[res-1].children[0]
                    eq_text = discharged['eq_text']
                    comp_text = discharged['comp_text']
                    calc.Load(eq_text,comp_text)
                elif 'func' in wt:
                    res = self.addFuncAux(loc,2)
                    func = self.layouts3[res-1].children[0]
                    eq_text = discharged['eq_text']
                    comp_text = discharged['comp_text']
                    func.Load(eq_text,comp_text)
                elif 'geo' in wt:
                    self.addGeoAux(loc,2)
                elif 'interp' in wt:
                    res = self.addAux(loc,2)
                    interp = self.layouts3[res-1].children[0]
                    prior = discharged['prior']
                    curr = discharged['curr']
                    interp.Load(prior, curr)
            

    def addAux(self, pos, dest):
        if dest is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()

            if self.interp < self.universalConstant:
                self.interp = self.interp + 1
                self.interpLoc.append(self.count)
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                w = InterpreterGui()
                w.restart_interpreter()
                layout.add_widget(w)
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
                return len(self.layouts)
            else:
                rem = self.interpLoc[0]
                #probably need to add another matrix to track which layout each is in
                self.interpLoc = self.interpLoc[1:-1]
                self.interpLoc.append(self.count)
                print(self.interpLoc)
                self.space1.ids.flone.remove_widget(self.layouts[rem])
                del self.layouts[rem]
        elif dest is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()

            if self.interp < self.universalConstant:
                self.interp = self.interp + 1
                self.interpLoc.append(self.count)
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                w = InterpreterGui()
                w.restart_interpreter()
                layout.add_widget(w)
                self.count2 += 1
                self.space2.ids.fltwo.add_widget(layout)
                self.layouts2.append(layout)
                return len(self.layouts2)
            else:
                rem = self.interpLoc[0]
                self.interpLoc = self.interpLoc[1:-1]
                self.interpLoc.append(self.count)
                print(self.interpLoc)
                self.space2.ids.fltwo.remove_widget(self.layouts2[rem])
                del self.layouts2[rem]
        elif dest is 2:
            if self.layouts3==[]:
                self.space3.ids.flthree.clear_widgets()

            if self.interp < self.universalConstant:
                self.interp = self.interp + 1
                self.interpLoc.append(self.count)
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                w = InterpreterGui()
                w.restart_interpreter()
                layout.add_widget(w)
                self.count3 += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)
                return len(self.layouts3)
            else:
                rem = self.interpLoc[0]
                self.interpLoc = self.interpLoc[1:-1]
                self.interpLoc.append(self.count)
                print(self.interpLoc)
                self.space3.ids.flthree.remove_widget(self.layouts3[rem])
                del self.layouts3[rem]

    def addFuncAux(self, pos, dest):
        if dest is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()
            if self.func < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(FunctionPlotter());
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
                return len(self.layouts)
        elif dest is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()
            if self.func < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(FunctionPlotter());
                self.count2 += 1
                self.space2.ids.fltwo.add_widget(layout)
                self.layouts2.append(layout)
                return len(self.layouts2)
        else:
            if self.layouts3==[]:
                self.space1.ids.flone.clear_widgets()
            if self.func < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(FunctionPlotter());
                self.count += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)
                return len(self.layouts3)

    def addCalcAux(self, pos, dest):
        if dest is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()
            if self.calc < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(Calculator());
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
                return len(self.layouts2)
        elif dest is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()
            if self.calc < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(Calculator());
                self.count2 += 1
                self.space2.ids.fltwo.add_widget(layout)
                self.layouts2.append(layout)
                return len(self.layouts2)
        else:
            if self.layouts3==[]:
                self.space3.ids.flthree.clear_widgets()
            if self.func < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(FunctionPlotter());
                self.count3 += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)
                return len(self.layouts3)

    def addGeoAux(self, pos, dest):
        if dest is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()
            if self.geo < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(Geometry());
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
                return len(self.layouts)
        elif dest is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()
            if self.geo < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(Geometry());
                self.count2 += 1
                self.space2.ids.fltwo.add_widget(layout)
                self.layouts2.append(layout)
                return len(self.layouts2)
        else:
            if self.layouts3==[]:
                self.space3.ids.flthree.clear_widgets()
            if self.geo < self.universalConstant:
                layout = FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(Geometry());
                self.count3 += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)
                return len(self.layouts3)


    def addTexAux(self, pos, dest):
        if dest is 0:
            if self.layouts==[]:
                self.space1.ids.flone.clear_widgets()

            if self.tex < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(Tex());
                self.count += 1
                self.space1.ids.flone.add_widget(layout)
                self.layouts.append(layout)
                return len(self.layouts)
        elif dest is 1:
            if self.layouts2==[]:
                self.space2.ids.fltwo.clear_widgets()
            if self.tex < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(Tex());
                self.count2 += 1
                self.space2.ids.fltow.add_widget(layout)
                self.layouts2.append(layout)
                return len(self.layouts2)
        else:
            if self.layouts3==[]:
                self.space3.ids.flthree.clear_widgets()
            if self.tex < self.universalConstant:
                layout =  FloatLayout(size_hint=(None,None), size = self.size, pos = pos)
                layout.add_widget(Tex());
                self.count3 += 1
                self.space3.ids.flthree.add_widget(layout)
                self.layouts3.append(layout)
                return len(self.layouts3)

    #Incorporationg writing functionality
    def clear(self):
        self.ids.pad.clear_canvas()

    def undo(self):
        self.ids.pad.undo()
    def redo(self):
        self.ids.pad.redo()

    def chColor(self):
        self.ids.pad.chColor()

class LiveManager(ScreenManager):
    pass

class WorkSpace1(Screen):
    pass

class WorkSpace2(Screen):
    pass

class WorkSpace3(Screen):
    pass

class WheatBlocksDropDownMenu(menu.MenuDropDown):
    pass

class WheatBlocksDropDownMenuButton(menu.MenuButton):
    dropdown_cls = ObjectProperty(WheatBlocksDropDownMenu)

class DrawDropDownMenu(menu.MenuDropDown):
    pass

class DrawDropDownMenuButton(menu.MenuButton):
    dropdown_cls = ObjectProperty(DrawDropDownMenu)