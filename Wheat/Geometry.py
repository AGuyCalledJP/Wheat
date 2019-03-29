from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import Ellipse

from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.lang import Builder


POINT_SIZE = .01

Builder.load_file('Geometry.kv')

class Geometry(ScatterLayout):
    move_lock = False
    scale_lock_left = False
    scale_lock_right = False
    scale_lock_top = False
    scale_lock_bottom = False

    def __init__(self, *args, **kwargs):
        super(Geometry, self).__init__(*args, **kwargs)
        self.size_hint = .5,.5
        # internals = PointLayout()
        # self.add_widget(internals)

    def on_touch_up(self, touch):
        self.size_hint = None, None
        self.move_lock = False
        self.scale_lock_left = False
        self.scale_lock_right = False
        self.scale_lock_top = False
        self.scale_lock_bottom = False
        self.size_hint = None,None
        if touch.grab_current is self:
            touch.ungrab(self)
            x = self.pos[0] / 10
            x = round(x, 0)
            x = x * 10
            y = self.pos[1] / 10
            y = round(y, 0)
            y = y * 10
            self.pos = x, y
            return super(Geometry, self).on_touch_up(touch)


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
            dx = dx
            dy = dy
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


class PointButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PointButton, self).__init__(**kwargs)

        self.source = 'visual_assets/fig_point.png'
        self.size = Image(source=self.source).texture.size
        self.selected = False

    def on_press(self):
        #TODO: case checking what mode we're in before "selecting" point
        if(self.selected == False):
            self.source = 'visual_assets/fig_point_selected.png'
            self.selected = True
        else:
            self.source = 'visual_assets/fig_point.png'
            self.selected = False


class PointLayout(ScatterLayout): #container for individual point, controls movement
    do_scale = False
    do_rotation = False
    do_translation = False

    def draw_unsel(self):
        with self.canvas:
            Color(1,1,1)
            # Ellipse(pos = self.pos, size=(30,30))


    def __init__(self, **kwargs):
        super(PointLayout, self).__init__(**kwargs)
        self.add_widget(PointButton())
        self.source = 'visual_assets/fig_point.png'
        self.size = Image(source=self.source).texture.size
        self.radius = (Image(source=self.source).texture.size[0])/2
        # self.size_hint_x = .1
        # self.size_hint_y = .1
        with self.canvas:
            Color(.5,1,0)
            Ellipse(pos=self.pos, size=(self.radius*2,self.radius*2))

        print(self.size)
        print(self.pos)

    # def collide_point(self, x, y):
    #
    #     if((x - self.x)**2 + (y - self.y)**2 < self.radius**2):
    #         return True
    #     return False


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':

                # Hold value of touch downed pos
                self.last_touch = touch.pos # Need this line
        return super(PointLayout, self).on_touch_down(touch)


    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':

                # process after movement or something?
                pass
        print(self.pos)
        return super(PointLayout, self).on_touch_up(touch)


    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                self.x = self.x + touch.pos[0] - self.last_touch[0] # Add the x distance between this mouse event and the last
                self.y = self.y + touch.pos[1] - self.last_touch[1] # Add the y distance between this mouse event and the last
                self.last_touch = touch.pos # Update the last position of the mouse
        return super(PointLayout, self).on_touch_move(touch)