from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

import math

from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle

from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.properties import (ObjectProperty, NumericProperty,
                             OptionProperty, BooleanProperty,
                             StringProperty, ListProperty)

Builder.load_file('Calculator.kv')

class Keyboard(GridLayout):
    pass

class Calculator(ScatterLayout):

    c1 = NumericProperty()
    c2 = NumericProperty()
    c3 = NumericProperty()
    c4 = NumericProperty()
    fontSizer = NumericProperty()

    c1 = 1
    c2 = .3
    c3 = .4
    c4 = .85
    fontSizer = 24

    equation_text = StringProperty()
    compute_text = StringProperty()
    keyboard = ObjectProperty()

    move_lock = False
    scale_lock_left = True
    scale_lock_right = True
    scale_lock_top = True
    scale_lock_bottom = True
    col = 1,1,1,1
    disp = 1

    def __init__(self, **kwargs):
        super(Calculator, self).__init__(**kwargs)
        self.size_hint = 0.4,0.5


    def on_touch_up(self, touch):
        self.size_hint = None,None
        self.move_lock = False
        self.scale_lock_left = False
        self.scale_lock_right = False
        self.scale_lock_top = False
        self.scale_lock_bottom = False
        if touch.grab_current is self:
            touch.ungrab(self)
            x = self.pos[0] / 10
            x = round(x, 0)
            x = x * 10
            y = self.pos[1] / 10
            y = round(y, 0)
            y = y * 10
            self.pos = x, y
            return super(Calculator, self).on_touch_up(touch)

    def transform_with_touch(self, touch):
        self.size_hint = None,None
        changed = False
        x = self.bbox[0][0]
        y = self.bbox[0][1]
        width = self.bbox[1][0]
        height = self.bbox[1][1]
        mid_x = x + width / 2
        mid_y = y + height / 2
        inner_width = width * 0.5
        inner_height = height * 0.5
        left = mid_x - (inner_width / 2)
        right = mid_x + (inner_width / 2)
        top = mid_y + (inner_height / 2)
        bottom = mid_y - (inner_height / 2)

            # just do a simple one finger drag
        if len(self._touches) == self.translation_touches:
            # _last_touch_pos has last pos in correct parent space,
            # just like incoming touch
            dx = (touch.x - self._last_touch_pos[touch][0]) \
                 * self.do_translation_x
            dy = (touch.y - self._last_touch_pos[touch][1]) \
                 * self.do_translation_y
            dx = dx / self.translation_touches
            dy = dy / self.translation_touches
            if (touch.x > left and touch.x < right and touch.y < top and touch.y > bottom or self.move_lock) and not self.scale_lock_left and not self.scale_lock_right and not self.scale_lock_top and not self.scale_lock_bottom:
                self.move_lock = True
                self.apply_transform(Matrix().translate(dx, dy, 0))
                changed = True

        change_x = touch.x - self.prev_x
        change_y = touch.y - self.prev_y
        anchor_sign = 1
        sign = 1
        if abs(change_x) >= 9 and not self.move_lock and not self.scale_lock_top and not self.scale_lock_bottom:
            if change_x < 0:
                sign = -1
            if (touch.x < left or self.scale_lock_left) and not self.scale_lock_right:
                self.scale_lock_left = True
                self.pos = (self.pos[0] + (sign * 10), self.pos[1])
                anchor_sign = -1
            elif (touch.x > right or self.scale_lock_right) and not self.scale_lock_left:
                self.scale_lock_right = True
            self.size[0] = self.size[0] + (sign * anchor_sign * 10)
            self.prev_x = touch.x
            changed = True
        if abs(change_y) >= 9 and not self.move_lock and not self.scale_lock_left and not self.scale_lock_right:
            if change_y < 0:
                sign = -1
            if (touch.y > top or self.scale_lock_top) and not self.scale_lock_bottom:
                self.scale_lock_top = True
            elif (touch.y < bottom or self.scale_lock_bottom) and not self.scale_lock_top:
                self.scale_lock_bottom = True
                self.pos = (self.pos[0], self.pos[1] + (sign * 10))
                anchor_sign = -1
            self.size[1] = self.size[1] + (sign * anchor_sign * 10)
            self.prev_y = touch.y
            changed = True
        return changed

    def on_touch_down(self, touch):
        self.size_hint = None,None
        x, y = touch.x, touch.y
        self.prev_x = touch.x
        self.prev_y = touch.y
        # if the touch isnt on the widget we do nothing
        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        # let the child widgets handle the event if they want
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if super(Scatter, self).on_touch_down(touch):
            # ensure children don't have to do it themselves
            if 'multitouch_sim' in touch.profile:
                touch.multitouch_sim = True
            touch.pop()
            self._bring_to_front(touch)
            return True
        touch.pop()

        # if our child didn't do anything, and if we don't have any active
        # interaction control, then don't accept the touch.
        if not self.do_translation_x and \
                not self.do_translation_y and \
                not self.do_rotation and \
                not self.do_scale:
            return False

        if self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        if 'multitouch_sim' in touch.profile:
            touch.multitouch_sim = True
        # grab the touch so we get all it later move events for sure
        self._bring_to_front(touch)
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos
        return True

    def flip(self):
        if self.disp == 1:
            self.keyboard.disabled = True;
            self.function.disabled = True;
            self.disp = 0
        else:
            self.keyboard.disabled = False;
            self.function.disabled = False;
            self.disp = 1


    def ClickedClear(self):
        self.equation_text = ""
        self.compute_text = ""
    def Clicked0(self):
        self.equation_text += "0"
        self.compute_text += "0"
    def ClickedPoint(self):
        self.equation_text += "."
        self.compute_text += "."
    def ClickedNeg(self):
        if (self.equation_text[0:1] == '-'):
            self.equation_text = self.equation_text[1:]
            self.compute_text = self.compute_text[1:]
        else:
            self.equation_text = "-" + self.equation_text
            self.compute_text = "-" + self.compute_text
    def ClickedEnter(self):
        split = self.compute_text.split('**(1/2)')
        result = split[0]
        for x in range (1,len(split)):
            if(split[x][0] == '('):
                i = split[x].index(')')
                result += split[x][0:i+1] + "**(1/2)" + split[x][i+1:]
            else:
                result += split[x][0] + "**(1/2)" + split[x][1:]
        self.compute_text = result
        try:
            ans = eval(self.compute_text)
            if(len(str(ans)) >= 10):
                self.equation_text = str(ans)[0:10]
                self.compute_text = str(ans)[0:10]
            else:
                self.equation_text = str(ans)
                self.compute_text = str(ans)
        except SyntaxError:
            self.equation_text = "SYNTAX Error"
            self.compute_text = "SYNTAX Error"

    # Line 2
    ########
    def ClickedLn(self):
        self.equation_text += "ln("
        self.compute_text += "math.log("
    def Clicked1(self):
        self.equation_text += "1"
        self.compute_text += "1"
    def Clicked2(self):
        self.equation_text += "2"
        self.compute_text += "2"
    def Clicked3(self):
        self.equation_text += "3"
        self.compute_text += "3"
    def ClickedPlus(self):
        self.equation_text += " + "
        self.compute_text += "+"

    # Line 3
    ########
    def Clickede(self):
        self.equation_text += "e"
        self.compute_text += "math.e"
    def Clicked4(self):
        self.equation_text += "4"
        self.compute_text += "4"
    def Clicked5(self):
        self.equation_text += "5"
        self.compute_text += "5"
    def Clicked6(self):
        self.equation_text += "6"
        self.compute_text += "6"
    def ClickedMinus(self):
        self.equation_text += " - "
        self.compute_text += "-"

    # Line 4
    ########
    def ClickedSquared(self):
        self.equation_text += u'\u00b2'
        self.compute_text += "**2"
    def Clicked7(self):
        self.equation_text += "7"
        self.compute_text += "7"
    def Clicked8(self):
        self.equation_text += "8"
        self.compute_text += "8"
    def Clicked9(self):
        self.equation_text += "9"
        self.compute_text += "9"
    def ClickedTimes(self):
        self.equation_text += " " + u'\u00d7' + " "
        self.compute_text += "*"

    # Line 5
    ########
    def ClickedExp(self):
        self.equation_text += "^"
        self.compute_text += "**"
    def ClickedInv(self):
        self.equation_text += "^(-1)"
        self.compute_text += "**(-1)"
    def ClickedLeftP(self):
        self.equation_text += "("
        self.compute_text += "("
    def ClickedRightP(self):
        self.equation_text += ")"
        self.compute_text += ")"
    def ClickedDiv(self):
        self.equation_text += " " + u'\u00f7' + " "
        self.compute_text += "/"


    # Line 6
    ########
    def ClickedSqrt(self):
        self.equation_text +=  u'\u221a'
        self.compute_text += "**(1/2)"
    def ClickedSin(self):
        self.equation_text += "sin("
        self.compute_text += "math.sin("
    def ClickedCos(self):
        self.equation_text += "cos("
        self.compute_text += "math.cos("
    def ClickedTan(self):
        self.equation_text += "tan("
        self.compute_text += "math.tan("
    def ClickedPi(self):
        self.equation_text += u'\u03c0'
        self.compute_text += "math.pi"

    def Save(self):
        letsGo = []
        letsGo.append(self.equation_text)
        letsGo.append(self.compute_text)
        return letsGo

    def Load(self, equation_text, compute_text):
        self.equation_text = equation_text
        self.compute_text = compute_text

# Notable Issues: Square root with math constants/functions, backspace wont work with those either
