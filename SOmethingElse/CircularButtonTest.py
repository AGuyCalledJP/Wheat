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
            Ellipse(pos = self.pos, size=(30,30))


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


class MyFloatLayout(FloatLayout):
    pass


class SampleApp(App):

    def build(self):

        f = MyFloatLayout()

        p = PointLayout()

        f.add_widget(p)
        return f


SampleApp().run()
