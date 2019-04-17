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

from Point import *
from GeomMenuing import *


#big todos:
# maybe make point moving not try to detect collision during movement, just check that we're grabbed?
    #fix redraw bug, but this^ should do that
# make operators do things
# points should be labeled both with an identifier and coords
# possibly allow adding points by numeric input?
#switching off of add mode during figure creation, or canceling creation, should remove all points from the in_prog figure

#selecting points should be added to some structure
#switching off of select mode should de-select all points
#selecting a selected point should remove it from the selection structure

#removing points from figure?
#clearing all figures?






Builder.load_file('Geometry.kv')

class Geometry(FloatLayout):


    ########################################
    ####    KV FORMATTING PROPERTIES    ####

    #Colours for use within geometry.kv
    white = [1,1,1,1]
    black = [0,0,0,1]

    button_bg_color = [.8,.1,.2,1]
    left_pane_bg_color = [.4, 0, 0, 1.]
    separator_color = left_pane_bg_color
    ########################################
    ########################################


    def change_mode(self, mode):
        if (mode != 'adding') and (mode != 'selecting') and (mode != 'moving'):
            print("ERROR: Invalid move change attempted, this should never happen.")
            return False
        elif self.mode_state != mode: #don't change mode if the new mode is the same as the current mode (prevents accidental resets)
            if self.mode_state == "adding":
                #if we switch off of adding and there's a figure in process, we need to address it
                # self.cancel_figure()
                self.make_figure()

            if self.mode_state == "selecting":
                #if we switch off of selecting, deselect everything:
                for selected in self.selected_points:
                    selected.select()

            self.mode_state = mode
            #resetting these just in case
            self.num_selected = 0
            self.in_prog_figure = None
            self.selected_points = []
            return True
        else:
            return False

    def make_figure(self):
        if self.in_prog_figure is None:
            return False
        self.in_prog_figure.draw_fig()
        #set the in progress figure pointer back to None
        self.in_prog_figure = None
        return True

    def cancel_figure(self):
        #don't try to cancel a figure creation with no actual points
        if self.in_prog_figure is None:
            return False
        self.in_prog_figure.clear_widgets()
        self.in_prog_figure = None
        return True

    def connect_interactive_space(self, interactive_space):
        self.interactive_space = interactive_space

    def touch_interactive_space(self, *args):
        #retrieve touch event
        contact_point = args[1].pos

        #are we in contact with the interactive space of the geometry widget?
        if self.interactive_space.collide_point(contact_point[0], contact_point[1]):
            #check mode
            if self.mode_state == 'adding':
                ## TODO: if the point we'd add is too close to the edge of interactive space, move it inwards more

                    #are we in the middle of making a figure?
                    if self.in_prog_figure is None:
                        #if not, create new figure
                        f = Figure()
                        self.in_prog_figure = f
                        self.interactive_space.add_widget(self.in_prog_figure)

                    #add point to it
                    self.in_prog_figure.add_point(contact_point[0], contact_point[1])
                    ## TODO: maybe put a label on it? either here or somewhere in the point itself
            else:
                #check if contact at point, if so continue
                if True:
                    if self.mode_state == 'selecting':
                         #if so select and add to some structure
                         #REMOVE: handled within pointbutton
                        pass
                    elif self.mode_state == 'moving':
                        #move point position, redraw figure
                        #REMOVE: handled within pointlayout
                        pass
                    else:
                        print("ERROR: Invalid mode_state interaction") #FIXME: remove if it turns out this never happens (it shouldn't)
                #otherwise, do nothing


    def __init__(self, *args, **kwargs):
        super(Geometry, self).__init__(*args, **kwargs)
        self.size_hint = .7,.7

        #the different modes the user can be in within the geometry app, defaults to adding
        self.mode_state = 'adding' #for some reason i can't get OptionProperty to behave correctly here, despite this being exactly the kind of situation you use it in.
        self.num_selected = 0 #number of points selected within select mode, not using NumericProperty for similar reasons as above
        self.selected_points = []

        self.interactive_space = None
        self.in_prog_figure = None #If we're in the middle of making a figure, this points to that in some way


    class Interactive_Space(FloatLayout): #class used to describe space containing points
        pass













"""
    A Figure contains a series of points that make up the shape they are meant to form. This can be a fully closed polygon, line segment, or point.
"""
class Figure(Widget):
    def draw_points(self):
        pass

    # def draw_line(self):
    def draw_fig(self):
        #traverse points to draw line of figure
        coords = []

        for p in self.children:
            coords.append(p.point_x)
            coords.append(p.point_y)

        self.canvas.remove(self.line_draw)
        new_line = InstructionGroup()
        new_line.add(Color(1,0,0))
        new_line.add(Line(points=coords, close=True, width=1.1))
        self.line_draw = new_line
        self.canvas.add(self.line_draw)
        return

    def calculateArea(self):

        # Based off of dszarkow's implementation of the Surveyor's Formula on codeproject.
        # Available at: https://www.codeproject.com/Articles/13467/A-JavaScript-Implementation-of-the-Surveyor-s-Form
        area = 0.0
        for i, p in enumerate(self.children): #for all points, enumerated as indices i
            x_diff = self.children[i+1].point_x - self.children[i].point_x
            x_diff = self.children[i+1].point_y - self.children[i].point_y
            area += self.children[i].point_x * y_diff - self.children[i].point_y * x_diff
        return 0.5 * area


    def calculatePerimeter(self):
        # Based off of dszarkow's implementation of the Surveyor's Formula on codeproject.
        # Available at: https://www.codeproject.com/Articles/13467/A-JavaScript-Implementation-of-the-Surveyor-s-Form
        perimeter = 0.0
        for i, p in enumerate(self.children): #for all points, enumerated as indices i
            x_diff = self.children[i+1].point_x - self.children[i].point_x
            x_diff = self.children[i+1].point_y - self.children[i].point_y
            perimeter += perimeter + (x_diff * x_diff + y_diff * y_diff)**0.5
        return perimeter


    def add_point(self, new_x, new_y):
        p = PointLayout(pos=[new_x-(img_size[0]/2), new_y-(img_size[0]/2)])
        self.add_widget(p)


    # TODO: add content
    def __init__(self, points = [], **kwargs):
        super(Figure, self).__init__(**kwargs)
        self.line_draw = InstructionGroup()

















######## The below code was in the Geometry class for scatter layout movements. Because the class should not move within current design intentions, this has been commented out.
######## I've moved the code here in case we end up needing it

    # move_lock = False
    # scale_lock_left = False
    # scale_lock_right = False
    # scale_lock_top = False
    # scale_lock_bottom = False

    # def on_touch_up(self, touch):
    #     self.size_hint = None, None
    #     self.move_lock = False
    #     self.scale_lock_left = False
    #     self.scale_lock_right = False
    #     self.scale_lock_top = False
    #     self.scale_lock_bottom = False
    #     self.size_hint = None,None
    #     if touch.grab_current is self:
    #         touch.ungrab(self)
    #         x = self.pos[0] / 10
    #         x = round(x, 0)
    #         x = x * 10
    #         y = self.pos[1] / 10
    #         y = round(y, 0)
    #         y = y * 10
    #         self.pos = x, y
    #         return super(Geometry, self).on_touch_up(touch)
    #
    # def transform_with_touch(self, touch):
    #     self.size_hint = None,None
    #     changed = False
    #     x = self.bbox[0][0]
    #     y = self.bbox[0][1]
    #     width = self.bbox[1][0]
    #     height = self.bbox[1][1]
    #     mid_x = x + width / 2
    #     mid_y = y + height / 2
    #     inner_width = width * 0.5
    #     inner_height = height * 0.5
    #     left = mid_x - (inner_width / 2)
    #     right = mid_x + (inner_width / 2)
    #     top = mid_y + (inner_height / 2)
    #     bottom = mid_y - (inner_height / 2)
    #
    #         # just do a simple one finger drag
    #     if len(self._touches) == self.translation_touches:
    #         # _last_touch_pos has last pos in correct parent space,
    #         # just like incoming touch
    #         dx = (touch.x - self._last_touch_pos[touch][0]) \
    #                 * self.do_translation_x
    #         dy = (touch.y - self._last_touch_pos[touch][1]) \
    #                 * self.do_translation_y
    #         dx = dx / self.translation_touches
    #         dy = dy / self.translation_touches
    #         dx = dx
    #         dy = dy
    #         if (touch.x > left and touch.x < right and touch.y < top and touch.y > bottom or self.move_lock) and not self.scale_lock_left and not self.scale_lock_right and not self.scale_lock_top and not self.scale_lock_bottom:
    #             self.move_lock = True
    #             self.apply_transform(Matrix().translate(dx, dy, 0))
    #             changed = True
    #
    #     change_x = touch.x - self.prev_x
    #     change_y = touch.y - self.prev_y
    #     anchor_sign = 1
    #     sign = 1
    #     if abs(change_x) >= 9 and not self.move_lock and not self.scale_lock_top and not self.scale_lock_bottom:
    #         if change_x < 0:
    #             sign = -1
    #         if (touch.x < left or self.scale_lock_left) and not self.scale_lock_right:
    #             self.scale_lock_left = True
    #             self.pos = (self.pos[0] + (sign * 10), self.pos[1])
    #             anchor_sign = -1
    #         elif (touch.x > right or self.scale_lock_right) and not self.scale_lock_left:
    #             self.scale_lock_right = True
    #         self.size[0] = self.size[0] + (sign * anchor_sign * 10)
    #         self.prev_x = touch.x
    #         changed = True
    #     if abs(change_y) >= 9 and not self.move_lock and not self.scale_lock_left and not self.scale_lock_right:
    #         if change_y < 0:
    #             sign = -1
    #         if (touch.y > top or self.scale_lock_top) and not self.scale_lock_bottom:
    #             self.scale_lock_top = True
    #         elif (touch.y < bottom or self.scale_lock_bottom) and not self.scale_lock_top:
    #             self.scale_lock_bottom = True
    #             self.pos = (self.pos[0], self.pos[1] + (sign * 10))
    #             anchor_sign = -1
    #         self.size[1] = self.size[1] + (sign * anchor_sign * 10)
    #         self.prev_y = touch.y
    #         changed = True
    #         return changed
    #
    # def on_touch_down(self, touch):
    #     self.size_hint = None,None
    #     x, y = touch.x, touch.y
    #     self.prev_x = touch.x
    #     self.prev_y = touch.y
    #     # if the touch isnt on the widget we do nothing
    #     if not self.do_collide_after_children:
    #         if not self.collide_point(x, y):
    #             return False
    #
    #     # let the child widgets handle the event if they want
    #     touch.push()
    #     touch.apply_transform_2d(self.to_local)
    #     if super(Scatter, self).on_touch_down(touch):
    #         # ensure children don't have to do it themselves
    #         if 'multitouch_sim' in touch.profile:
    #             touch.multitouch_sim = True
    #         touch.pop()
    #         self._bring_to_front(touch)
    #         return True
    #     touch.pop()
