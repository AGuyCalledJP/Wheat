from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import Ellipse
from kivy.graphics import Line
from kivy.graphics import InstructionGroup
from kivy.properties import (ObjectProperty, NumericProperty,
                             OptionProperty, BooleanProperty,
                             StringProperty, ListProperty)

from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.lang import Builder


img_source_selected = 'visual_assets/fig_point_selected.png'
img_source = 'visual_assets/fig_point.png'
img_size = Image(source=img_source).texture.size

class PointButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PointButton, self).__init__(**kwargs)

        self.source = img_source
        self.size = Image(source=self.source).texture.size
        self.selected = False

    '''
        Checks if the button is selected or not, and flips to the other state, while updating the image to reflect whether the point is selected
    '''
    def select(self):
        geom = self.parent.parent.parent.parent.parent.parent.parent.parent
        if(geom.mode_state == "selecting"): #TODO: please god make this prettier
            if(self.selected == False):
                self.source = img_source_selected
                geom.num_selected+=1
                self.selected = True
                geom.selected_points.append(self) #we add/remove the parent of the pointbutton, the layout containing it, since that has the proper coordinates
                print("selecting point, points now at " + str(geom.num_selected))
                print("selpoints length : " + str(len(geom.selected_points)))
            else:
                self.source = img_source
                geom.num_selected-=1
                self.selected = False
                geom.selected_points.remove(self) #we add/remove the parent of the pointbutton, the layout containing it, since that has the proper coordinates
                print("deselecting point, points now at " + str(geom.num_selected))
                print("selpoints length : " + str(len(geom.selected_points)))

    '''
        If contact is made with the button, selects it. Possibly to be removed and have contact handled above it.
    '''
    def on_press(self):
        #TODO: case checking what mode we're in before "selecting" point
        self.select()



class PointLayout(ScatterLayout): #container for individual point, controls movement
    do_scale = False
    do_rotation = False
    do_translation = False

    def __init__(self, **kwargs):
        super(PointLayout, self).__init__(**kwargs)
        self.add_widget(PointButton())
        self.source = img_source
        self.size = Image(source=self.source).texture.size
        self.radius = (Image(source=self.source).texture.size[0])/2 #radius of point, based off size of image (image is assumed to be a square canvas with a circle of diameter equal to image width and height)
        self.size_hint_x = None
        self.size_hint_y = None
        self.point_x = self.pos[0] + self.radius # visual center of point (center of the image)
        self.point_y = self.pos[1] + self.radius # visual center of point (center of the image)
        self.last_touch = [0,0]

    '''
        Selects all (ideally, the singular) children of this layout container.
    '''
    def select_children(self):
        for child in self.content.children: #NOTE: Because this was originally a ScatterLayout, we need to use content.children instead of children
            child.select()

    def collide_point(self, x, y): #Checks for contact within the radius of the point
        if((x - self.point_x)**2 + (y - self.point_y)**2 < self.radius**2):
            return True
        return False


    def on_touch_down(self, touch):
        #include check for move mode
        if(self.parent.parent.parent.parent.parent.parent.mode_state == "moving"):
            if self.collide_point(*touch.pos):
                if touch.button == 'left':

                    # Hold value of touch downed pos
                    self.last_touch = touch.pos # Need this line
        return super(PointLayout, self).on_touch_down(touch)


    def on_touch_up(self, touch):
        if(self.parent.parent.parent.parent.parent.parent.mode_state == "moving"):
            if self.collide_point(*touch.pos):
                if touch.button == 'left':
                    # move complete TODO: find some way to have figure update for this
                    self.parent.draw_fig()
                    pass
        return super(PointLayout, self).on_touch_up(touch)


    def on_touch_move(self, touch):
        if(self.parent.parent.parent.parent.parent.parent.mode_state == "moving"):
            if self.collide_point(*touch.pos):
                if touch.button == 'left':
                    self.x = self.x + touch.pos[0] - self.last_touch[0] # Add the x distance between this mouse event and the last
                    self.y = self.y + touch.pos[1] - self.last_touch[1] # Add the y distance between this mouse event and the last
                    self.point_x = self.pos[0] + self.radius
                    self.point_y = self.pos[1] + self.radius
                    self.last_touch = touch.pos # Update the last position of the mouse
        return super(PointLayout, self).on_touch_move(touch)
