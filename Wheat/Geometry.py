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
from kivy.properties import (ObjectProperty, NumericProperty,
                             OptionProperty, BooleanProperty,
                             StringProperty, ListProperty)



img_source_selected = 'visual_assets/fig_point_selected.png'
img_source = 'visual_assets/fig_point.png'
img_size = Image(source=img_source).texture.size



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

            #todo: if the mode state changes from adding and there are points added from a figure, issue a make figure call

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
        # internals = PointLayout()
        # self.add_widget(internals)

        #the different modes the user can be in within the geometry app, defaults to adding
        self.mode_state = 'adding' #for some reason i can't get OptionProperty to behave correctly here, despite this being exactly the kind of situation you use it in.
        self.num_selected = 0 #number of points selected within select mode, not using NumericProperty for similar reasons as above
        self.selected_points = []

        self.interactive_space = None
        self.in_prog_figure = None #If we're in the middle of making a figure, this points to that in some way


    class Interactive_Space(FloatLayout):
        pass





class RightPane(FloatLayout):

    def hide_pane(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
                return 1 #return values indicate size the header should be in th kv file, which runs this and sets header's size_hint to this value
        #capture sizing information, opacity, disabled status, and set to 0's/None/True to hide the pane
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True
            return .66 #return values indicate size the header should be in th kv file, which runs this and sets header's size_hint to this value


#this might need to live somewhere else

class OppButton(Button):

    def hide_opp(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        #capture sizing information, opacity, disabled status, and set to 0's/None/True to hide the pane
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

    def __init__(self, **kwargs):
        super(OppButton, self).__init__(**kwargs)
        self.hide_opp() #start hidden, use when we have add functionality working



class MakeFigureButton(Button):
    def hide_make(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        #capture sizing information, opacity, disabled status, and set to 0's/None/True to hide the pane
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

    def __init__(self, **kwargs):
        super(MakeFigureButton, self).__init__(**kwargs)
        # self.hide_make() #start hidden, use when we have add functionality working




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
        new_line.add(Line(points=coords, close=True, width=1.5))
        self.line_draw = new_line
        self.canvas.add(self.line_draw)
        return

    # def draw_fig(self):
    #     self.canvas.remove_group()
    #     self.draw_line()
    #     # self.draw_points()
    #     return


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
        # print("point added at " + str(new_x) + ", " + str(new_y))


    # TODO: add content
    def __init__(self, points = [], **kwargs):
        super(Figure, self).__init__(**kwargs)
        self.line_draw = InstructionGroup()
        # for p in points:
        #     self.add_point(p[0],p[1])
        # self.draw_fig()








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
                geom.selected_points.append(self.parent) #we add/remove the parent of the pointbutton, the layout containing it, since that has the proper coordinates
            else:
                self.source = img_source
                geom.num_selected-=1
                self.selected = False
                geom.selected_points.remove(self.parent) #we add/remove the parent of the pointbutton, the layout containing it, since that has the proper coordinates

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
