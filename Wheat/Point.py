from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.label import Label
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

class PointLabel(Label):
    def __init__(self, **kwargs):
        super(PointLabel, self).__init__(**kwargs)
        self.pos = [img_size[0]*-1, 0]
        # [-40, -20] #for use with 22x22

class PointButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PointButton, self).__init__(**kwargs)
        self.lab = PointLabel()
        self.add_widget(self.lab)
        self.source = img_source
        self.size = Image(source=self.source).texture.size
        self.selected = False

    '''
        Sets point label's text
    '''
    def set_lab(self, new_lab):
        self.lab.identifier = str(new_lab)
        self.lab.text = str(new_lab)
    '''
    Retrieves label's text
    '''
    def get_lab(self):
        return self.lab.identifier


    '''
        Checks if the button is selected or not, and flips to the other state, while updating the image to reflect whether the point is selected
    '''
    def select(self):
        geom = self.parent.parent.parent.parent.parent.parent.parent.parent.parent

        if(geom.mode_state == "selecting"):
            if(self.selected == False):
                self.source = img_source_selected
                geom.num_selected+=1
                self.selected = True
                geom.selected_points.append(self.parent.parent) #we add/remove the parent of the pointbutton, the layout containing it, since that has the proper coordinates
            else:
                self.source = img_source
                geom.num_selected-=1
                self.selected = False
                geom.selected_points.remove(self.parent.parent) #we add/remove the parent of the pointbutton, the layout containing it, since that has the proper coordinates
            #send a select event
            geom.select_event()

    '''
        Forces a point to be deselected, without altering the selected points or num selected in Geometry.
        Used to prevent altering the list of selected points while traversing.
        After use, selected_points and num_selected should be updated within Geometry.
    '''
    def set_as_deselected(self):
        self.source = img_source
        self.selected = False

    '''
        If contact is made with the button, selects it. Possibly to be removed and have contact handled above it.
    '''
    def on_press(self):
        self.select()



class PointLayout(ScatterLayout): #container for individual point, controls movement


    def __init__(self, **kwargs):
        super(PointLayout, self).__init__(**kwargs)
        self.p = PointButton()
        self.add_widget(self.p)
        self.source = img_source
        self.size = Image(source=self.source).texture.size
        self.radius = (Image(source=self.source).texture.size[0])/2 #radius of point, based off size of image (image is assumed to be a square canvas with a circle of diameter equal to image width and height)
        self.size_hint_x = None
        self.size_hint_y = None

        # virtual visual center of point (center of the image)
        self.v_point_x = None
        self.v_point_y = None
        self.i_s = None # this will point to the interactive space after we've been added to a figure

        # actual visual center of point (center of the image)
        self.a_point_x = self.pos[0] + self.radius
        self.a_point_y = self.pos[1] + self.radius

        self.last_touch = [0,0]
        self.compare = 0 #THIS VALUE IS USED EXCLUSIVELY FOR CCW SORTING ABOUT CENTER OF AN ARBITRARY SERIES OF POINTS

    '''
        Sets point label's text
    '''
    def set_lab(self, new_lab):
        self.p.set_lab(new_lab)

    '''
        Deselects point.
    '''
    def set_as_deselected(self):
        self.p.set_as_deselected()

    '''
        Selects all (ideally, the singular) children of this layout container.
    '''
    def select_children(self):
        for child in self.content.children: #NOTE: Because this was originally a ScatterLayout, we need to use content.children instead of children
            child.select()

    '''
        Checks for contact within the radius of the point
    '''
    def collide_point(self, x, y):
        if((x - self.a_point_x)**2 + (y - self.a_point_y)**2 < self.radius**2):
            return True
        return False


    def on_touch_down(self, touch):
        geom = self.parent.parent.parent.parent.parent.parent.parent
        #include check for move mode
        if(geom.mode_state == "moving"):
            if self.collide_point(*touch.pos):
                # Hold value of touch downed pos
                self.last_touch = touch.pos # Need this line
        return super(PointLayout, self).on_touch_down(touch)

    '''
        Moves point to stay into the interactive space boundaries.
    '''
    def correct_position(self, coords):
        south = self.i_s.pos[1]
        west = self.i_s.pos[0]
        north = self.i_s.pos[1] + self.i_s.size[1] - 2*self.radius
        east = self.i_s.pos[0] + self.i_s.size[0] - 2*self.radius

        x = coords[0]
        y = coords[1]

        if x < west:    x = west
        if x > east:    x = east
        if y < south:   y = south
        if y > north:   y = north

        self.pos = [x,y]

    '''
        Sets 'Virtual Coordinates'
    '''
    def set_relative_pos(self):
        self.i_s = self.parent.parent.parent.parent.parent.parent.parent.interactive_space
        self.v_point_x = self.a_point_x - self.i_s.pos[0]
        self.v_point_y = self.a_point_y - self.i_s.pos[1]

    def on_touch_up(self, touch):
        if(self.parent.parent.parent.parent.parent.parent.parent.mode_state == "moving"):
            self.parent.draw_fig()
             #NOTE: This DOESN'T check collision on point before running this, which may cause a major loss of performance.
             #if so, check collision within the geometry widget as a whole
            if self.collide_point(*touch.pos):
                pass
        return super(PointLayout, self).on_touch_up(touch)


    def on_touch_move(self, touch):
        if(self.parent.parent.parent.parent.parent.parent.parent.mode_state == "moving"):
            if self.collide_point(*touch.pos):
                self.x = self.x + touch.pos[0] - self.last_touch[0] # Add the x distance between this mouse event and the last
                self.y = self.y + touch.pos[1] - self.last_touch[1] # Add the y distance between this mouse event and the last

                correction = self.correct_position([self.x, self.y])

                #update virtual
                self.v_point_x = (self.pos[0] + self.radius) - self.i_s.pos[0]
                self.v_point_y = (self.pos[1] + self.radius) - self.i_s.pos[1]

                #update actual
                self.a_point_x = self.pos[0] + self.radius
                self.a_point_y = self.pos[1] + self.radius

                self.last_touch = touch.pos # Update the last position of the mouse
        return super(PointLayout, self).on_touch_move(touch)
