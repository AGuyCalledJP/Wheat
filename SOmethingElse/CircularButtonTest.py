from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color

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
        self.source = 'visual_assets/fig_point.png'
        self.selected = False


    # def on_touch_down(self, touch):
    #     return False

    def collide_point(self,x,y): # override of existing

        if( ((self.pos[0] - x)**2 + (self.pos[1] - y)**2) == 10**2): #if the distance between the given point and this point is less than the radius of the visual circle around the point, we have collision
            print("proper collision")
            return True
        else:
            print("no collision")
            return False

    # def on_touch_down(self, touch):
    #     if(self.selected == False):
    #         self.source = 'visual_assets/fig_point_selected.png'
    #         self.selected = True
    #     else:
    #         self.source = 'visual_assets/fig_point.png'
    #         self.selected = True
    #     return False
    #
    #
    # def on_touch_move(self, touch):
    #     if(collide_point(touch.x, touch.y)):
    #         do_translation()
    #     return False


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            if(self.selected == False):
                print("ran1")
                self.source = 'visual_assets/fig_point_selected.png'
                self.selected = True
            else:
                print("ran2")
                self.source = 'visual_assets/fig_point.png'
                self.selected = True
            # do whatever else here

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            do_translation = True
            pass
            # now we only handle moves which we have grabbed

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            # and finish up here


class PointLayout(ScatterLayout):
    do_scale = False
    do_rotation = False
    do_translation = False
    def __init__(self, **kwargs):
        super(PointLayout, self).__init__(**kwargs)
        self.width = POINT_SIZE
        self.height = POINT_SIZE
        with self.canvas:
            Color(1,0,1)


class MyFloatLayout(FloatLayout):
    pass


class SampleApp(App):

    def build(self):

        f = MyFloatLayout()
        with f.canvas:
            Color(0,0,1)
        p = PointLayout()
        p.add_widget(PointButton())
        with p.canvas:
            Color(1,0,0)
        f.add_widget(p)

        return f


SampleApp().run()
