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
from kivy.lang import Builder

class MyCodeInput(CodeInput):

    def __init__(self, size, **kwargs):
        super(MyCodeInput, self).__init__(**kwargs)
        x = size[0]
        y = size[1]
        chunk = x * .30
        self.size_hint = (None,None)
        self.size = (x - chunk,y)
        # self.pos = (10,0)
        self.pos_hint = {'x': .15, 'y': 0}
        self.lexer = CythonLexer()

    def Deactivate(self):
        self.disabled = True
    
    def Activate(self):
        self.disabled = False
    
    def update(self, size):
        x = size[0]
        y = size[1]
        print("code")
        print(x)
        chunk = x * .30
        self.size_hint = (None,None)
        self.size = (x - chunk,y)

class MyButton(Button):

    def __init__(self, size, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        x = size[0]
        y = size[1]
        chunk = x * .85
        self.size_hint = (None, None)
        self.size = (x - chunk,y)
        # self.pos = (690,0)
        self.pos_hint = {'x': .85, 'y': 0}
        # self.size_hint = (.15,1)
        self.text = "Move"
    
    def update(self, size):
        x = size[0]
        y = size[1]
        print("button")
        print(x)
        chunk = x * .85
        self.size_hint = (None, None)
        self.size = (x - chunk,y)

class MyCheckBox(CheckBox):

    def __init__(self, size, **kwargs):
        super(MyCheckBox, self).__init__(**kwargs)
        self.pos_hint = {'x': 0, 'y': 0}
        x = size[0]
        y = size[1]
        chunk = x * .85
        self.size_hint = (None, None)
        self.size = (x - chunk,y)

    def Deactivate(self):
        self.disabled = True
    
    def Activate(self):
        self.disabled = False
    
    def update(self, size):
        self.pos_hint = {'x': 0, 'y': 0}
        x = size[0]
        y = size[1]
        chunk = x * .85
        self.size_hint = (None, None)
        self.size = (x - chunk,y)

class MyRunButton(Button):

    def __init__(self, size, **kwargs):
        super(MyRunButton, self).__init__(**kwargs)
        x = size[0]
        y = size[1]
        chunk = x * .85
        self.size_hint = (None, None)
        self.size = (x - chunk,y/2)
        # self.pos = (690,0)
        self.pos_hint = {'x': .85, 'y': 0}
        # self.size_hint = (.15,1)
        self.text = "Run"
    
    def update(self, size):
        x = size[0]
        y = size[1]
        chunk = x * .85
        self.size_hint = (None, None)
        self.size = (x - chunk,y/2)


class MyScatterLayout(ScatterLayout):
    move_lock = False
    scale_lock_left = False
    scale_lock_right = False
    scale_lock_top = False
    scale_lock_bottom = False
    col = 1,1,1,1
    disp = 1

    def __init__(self, **kwargs):
        super(MyScatterLayout, self).__init__(**kwargs)
        self.size = (800,400)
        self.pos = (400,400)
        self.size_hint = (None, None)
        self.check = MyCheckBox(self.size, id = "check")
        self.code = MyCodeInput(self.size, id = "code")
        self.move = MyButton(self.size, id = "switch") 
        self.run = MyRunButton(self.size, id = "run")
        self.move.bind(on_press=self.flip)
        self.add_widget(self.check)
        self.add_widget(self.code)
        self.add_widget(self.move)
        self.add_widget(self.run)
        

    def flip(self, button):
        if self.disp:
            self.disp = 0
        else:
            self.disp = 1
        self.flipTheSwitch()

    def flipTheSwitch(self):
        if self.disp:
            self.check.Deactivate()
            self.code.Deactivate()

        else:
            self.check.Activate()
            self.code.Activate()
    
    def on_touch_up(self, touch):
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
            return super(MyScatterLayout, self).on_touch_up(touch)

    def transform_with_touch(self, touch):
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
        if changed:
            self.check.update(self.size)
            self.code.update(self.size)
            self.move.update(self.size)
        return changed

    def on_touch_down(self, touch):
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
        print(self.size)
        return True

class WheatBlock(FloatLayout):

    def __init__(self, **kwargs):
        super(WheatBlock, self).__init__(**kwargs)
        self.s = MyScatterLayout(do_rotation=False)
        self.add_widget(self.s)

