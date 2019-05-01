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

from pdf2image import convert_from_path
from pylatex import Document, Section, Subsection, Command, Math, Alignat, errors
from PIL import Image
import os
import sys

Builder.load_file('Tex.kv')

default = 'Wheat/widget_visuals/LaTeX_logo.png'
ran = 'Wheat/Notebook/Tex/cropped'
end = '.png'

class Bar(FloatLayout):
    pass

class Display(FloatLayout):
    start = None
    def __init__(self, where, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.pos_hint = {'x' : 0.025, 'y' : 0.175}
        self.size_hint = .95, 0.6
        if self.start is None:
            with self.canvas:
                self.bg = Rectangle(source = where, pos=self.pos, size=self.size)
            self.bind(pos=self.update_bg)
            self.bind(size=self.update_bg)

    def update(self):
        with self.canvas:
            self.canvas.ask_update()

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def bye(self):
        self.parent.remove_widget(self)

class Input(FloatLayout):
    def hide_input(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
                #return 1

        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True
            #return .85


class Tex(ScatterLayout):

    c1 = NumericProperty()
    c2 = NumericProperty()
    c3 = NumericProperty()
    c4 = NumericProperty()
    fontSizer = NumericProperty()
    counter = NumericProperty()
    counter = 0

    c1 = 1
    c2 = .3
    c3 = .4
    c4 = .85
    fontSizer = 24

    code = StringProperty()
    disp = ObjectProperty()
    docname = StringProperty()
    docname = "latex"

    move_lock = False
    scale_lock_left = False
    scale_lock_right = False
    scale_lock_top = False
    scale_lock_bottom = False
    col = 1,1,1,1
    disp = 1
    count = 0

    def __init__(self, **kwargs):
        super(Tex, self).__init__(**kwargs)
        self.size_hint = 0.5,0.3
        self.disp = Display(default)
        self.add_widget(self.disp)

    def update(self):
        with self.canvas:
            self.canvas.ask_update()

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
            return super(Tex, self).on_touch_up(touch)

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
        parent = self.parent.parent
        me = self.parent
        parent.remove_widget(me)
        parent.add_widget(me)
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


    def fill_document(self,doc,code):
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(r"\nonstopmode")
                agn.append(code)


    def write(self):
        if os.path.exists("latex.aux"):
            os.remove("latex.aux")
            os.remove("latex.log")
            os.remove("latex.tex")
            os.remove("latex.pdf")
        else:
            print("The file does not exist")

        print(self.counter)
        self.code = self.ids.equation.text
        doc = Document(self.docname)
        self.fill_document(doc,self.code)
        try:
            print("it tried")
            doc.generate_pdf(filepath='Wheat/Notebook/Tex/', clean_tex = True, compiler='lualatex') #not good with error
            print("it tried2")
            self.convert_image(False)
        except:
            pass

    def convert_image(self,tex_error):

        if not tex_error:
            pages = convert_from_path('Wheat/Notebook/Tex/latex.pdf', 500)
            for page in pages:
                page.save('Wheat/Notebook/Tex/output.png', 'PNG')

            self.crop('Wheat/Notebook/Tex/output.png')
        else:
            self.updateDisp('Wheat/Notebook/Tex/error.png')
            print('here')

    def crop(self, filename):

        image_obj = Image.open(filename)
        width, height = image_obj.size
        coords = (0.4*width, 0.17*height, 0.63*width, 0.21*height)
        cropped_image = image_obj.crop(coords)
        dest = ran + str(self.count) + end
        cropped_image.save(dest)
        self.count += 1
        self.updateDisp(dest)

    def updateDisp(self, dest):
        self.disp.bye()
        self.remove_widget(self.disp)
        self.disp.update()
        self.disp = Display(dest)
        self.add_widget(self.disp)
        self.disp.update()
        self.update()
        if self.count > 1:
            self.clean()

    def clean(self):
        rem = ran + str(self.count - 1) + end
        os.remove(rem)
