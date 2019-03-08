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


POINT_SIZE = .01

class PointButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PointButton, self).__init__(**kwargs)
        # with self.canvas:
        #     Color(.5,.5,0)
        #     Rectangle(size=self.size)
        self.source = 'visual_assets/fig_point.png'
        self.size = Image(source=self.source).texture.size
        self.selected = False
        # self.size_hint_x = 1
        # self.size_hint_y = 1
        # self.width = 30
        # self.height = 30
        print("point")
        print(self.size)
        print(self.pos)


    # def collide_point(self,x,y): # override of existing
    #
    #     if( ((self.pos[0] - x)**2 + (self.pos[1] - y)**2) < 15**2): #if the distance between the given point and this point is less than the radius of the visual circle around the point, we have collision
    #         print("proper collision")
    #         return True
    #     else:
    #         print("no collision")
    #         return False
    #
    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         if touch.button == 'left':
    #
    #             # Hold value of touch downed pos
    #             return super(PointButton, self).on_touch_down(touch)
    #
    #     return super(PointButton, self).on_touch_down(touch)
    #
    # def on_touch_move(self, touch):
    #     if self.collide_point(*touch.pos):
    #         if touch.button == 'left':
    #             self.x = touch.dpos[0]
    #             self.y = touch.dpos[1]
    #
    #     return super(PointButton, self).on_touch_move(touch)
    #
    # def on_touch_up(self, touch):
    #     if self.collide_point(*touch.pos):
    #         if touch.button == 'left':
    #
    #             # process after movement or something?
    #             pass
    #
    #     return super(PointButton, self).on_touch_up(touch)










    def on_press(self):
        # if self.collide_point(*touch.pos):
        #     # touch.grab(self)
        #     if(self.selected == False):
        #         print("ran1")
        #         self.source = 'visual_assets/fig_point_selected.png'
        #         self.selected = True
        #     else:
        #         print("ran2")
        #         self.source = 'visual_assets/fig_point.png'
        #         self.selected = False
        if(self.selected == False):
            print("ran1")
            self.source = 'visual_assets/fig_point_selected.png'
            self.selected = True
        else:
            print("ran2")
            self.source = 'visual_assets/fig_point.png'
            self.selected = False

            # do whatever else here
    #
    # def on_touch_move(self, touch):
    #     if touch.grab_current is self:
    #         do_translation = True
    #         pass
    #         # now we only handle moves which we have grabbed
    #
    # def on_touch_up(self, touch):
    #     if touch.grab_current is self:
    #         touch.ungrab(self)
    #         # and finish up here


class PointLayout(ScatterLayout): #container for individual point, controls movement
    do_scale = False
    do_rotation = False
    do_translation = False

    def draw_unsel(self):
        with self.canvas:
            Color(1,1,1)
            Ellipse(pos = self.pos, size=(30,30))


    def __init__(self, **kwargs):
        super(PointLayout, self).__init__(**kwargs)

        self.source = 'visual_assets/fig_point.png'
        self.size = Image(source=self.source).texture.size
        # self.width = 30
        # self.height = 30
        self.size_hint_x = .1
        self.size_hint_y = .1
        # with self.canvas:
        #     Color(1,0,1)
        #     Ellipse(size=self.size)

        print(self.size)
        print(self.pos)

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
        with self.canvas:
            Color(1,0,1)
            Rectangle(size=self.size)
        return super(PointLayout, self).on_touch_move(touch)

    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         touch.grab(self)
    # def on_touch_move(self, touch):
    #     if touch.grab_current is self:
    #         do_translation = True
    #         pass
    #         # now we only handle moves which we have grabbed
    #
    # def on_touch_up(self, touch):
    #     if touch.grab_current is self:
    #         touch.ungrab(self)
    #         # and finish up here




class MyFloatLayout(FloatLayout):
    pass


class SampleApp(App):

    def build(self):

        f = MyFloatLayout()

        p = PointLayout()
        p.add_widget(PointButton())

        f.add_widget(p)
        return f


SampleApp().run()
