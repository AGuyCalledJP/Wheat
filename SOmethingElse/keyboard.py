from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout


from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle

from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.lang import Builder
from kivy.base import runTouchApp

Builder.load_file('keyboard.kv')

class Keyboard(GridLayout):
    text = ""

    def __init___(self, *args, **kwargs):
        super(Keyboard, self).__init__(*args, **kwargs)

    def ClickedClear(self):
        self.text = ""
    def Clicked0(self):
        self.text += "0"
    def ClickedPoint(self):
        self.text += "."
    def ClickedNeg(self):
        self.text += "-"
    def ClickedEnter(self):
        print(self.text)

    # Line 2
    ########
    def ClickedDel(self):
        self.text = self.text[:-1]
    def Clicked1(self):
        self.text += "1"
    def Clicked2(self):
        self.text += "2"
    def Clicked3(self):
        self.text += "3"
    def ClickedPlus(self):
        self.text += " + "

    # Line 3
    ########
    def Clickedx(self):
        self.text += "x"
    def Clicked4(self):
        self.text += "4"
    def Clicked5(self):
        self.text += "5"
    def Clicked6(self):
        self.text += "6"
    def ClickedMinus(self):
        self.text += " - "

    # Line 4
    ########
    def ClickedSquared(self):
        self.text += "**2"
    def Clicked7(self):
        self.text += "7"
    def Clicked8(self):
        self.text += "8"
    def Clicked9(self):
        self.text += "9"
    def ClickedTimes(self):
        self.text += "*"

    # Line 5
    ########
    def ClickedExp(self):
        self.text += "**"
    def ClickedInv(self):
        self.text += "**(-1)"
    def ClickedLeftP(self):
        self.text += "("
    def ClickedRightP(self):
        self.text += ")"
    def ClickedDiv(self):
        self.text += "/"

    # Line 6
    ########
    def ClickedSqrt(self):
        self.text += "**(-1/2)"
    def ClickedSin(self):
        self.text += "sin"
    def ClickedCos(self):
        self.text += "cos"
    def ClickedTan(self):
        self.text += "tan"
    def ClickedPi(self):
        self.text += "pi"

##########################################################################
# Compiler Type Runner Thing                                             #
##########################################################################

class KeyboardTest(App):
    title = 'Math Type'

    def build(self):
        return Keyboard()

if __name__ == '__main__':
    KeyboardTest().run()

##########################################################################
