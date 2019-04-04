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
from kivy.properties import (ObjectProperty, NumericProperty,
                             OptionProperty, BooleanProperty,
                             StringProperty, ListProperty)


img_source = 'visual_assets/fig_point.png'
img_size = Image(source=img_source).texture.size



Builder.load_file('Geometry.kv')

class Geometry(ScatterLayout):
    move_lock = False
    scale_lock_left = False
    scale_lock_right = False
    scale_lock_top = False
    scale_lock_bottom = False

    ########################################
    ####    KV FORMATTING PROPERTIES    ####
    white = [1,1,1,1]
    black = [0,0,0,1]

    button_bg_color = [.8,.1,.2,1]
    left_pane_bg_color = [.4, 0, 0, 1.]
    separator_color = left_pane_bg_color
    ########################################
    ########################################



    ########################################
    ####        MENU PROPERTIES         ####

    mode_state = OptionProperty('adding', options=['moving',
                                                   'selecting',
                                                   'adding'])
    hiding_buttons = BooleanProperty(False)

    ########################################
    ########################################

    def __init__(self, *args, **kwargs):
        super(Geometry, self).__init__(*args, **kwargs)
        self.size_hint = .7,.7
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


    def hide_buttons(self):
        #look up right pane
        if hiding_buttons:
            #set size_hint of right pane to 0
            pass
        else:
            #set size_hint to original value
            pass
        pass

    def check_boundaries(self, x,y):
        ## TODO: given x and y, are we within the interactive_space
        pass






"""
    A Figure contains a series of points that make up the shape they are meant to form. This can be a fully closed polygon, line segment, or point.
"""
class Figure(Widget):
    def draw_points(self):
        pass

    def draw_line(self):
        #traverse points to draw line of figure
        coords = []

        for p in self.children:
            coords.append(p.point_x)
            coords.append(p.point_y)

        with self.canvas:
            Color(1,0,0) #WHITE
            Line(coords)
        return

    def draw_fig(self):
        if(self.canvas):
            self.canvas.clear() #remove all previous points and lines on this figure (this hopefully only effects one figure?)
        self.draw_line()
        # self.draw_points()
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
        p = PointLayout(pos=[new_x-(img_size/2), new_y-(img_size/2)])
        self.add_widget(p)


    # TODO: add content
    def __init__(self, points):
        for p in points:
            self.add_point(p[0],p[1])
        self.draw_fig()








class PointButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PointButton, self).__init__(**kwargs)

        self.source = 'visual_assets/fig_point.png'
        self.size = Image(source=self.source).texture.size
        self.selected = False

    '''
        Checks if the button is selected or not, and flips to the other state, while updating the image to reflect whether the point is selected
    '''
    def select(self):
        if(self.selected == False):
            self.source = 'visual_assets/fig_point_selected.png'
            self.selected = True
        else:
            self.source = 'visual_assets/fig_point.png'
            self.selected = False

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
        self.source = 'visual_assets/fig_point.png'
        self.size = Image(source=self.source).texture.size
        self.radius = (Image(source=self.source).texture.size[0])/2 #radius of point, based off size of image (image is assumed to be a square canvas with a circle of diameter equal to image width and height)
        self.size_hint_x = None
        self.size_hint_y = None
        self.point_x = self.pos[0] + self.radius # visual center of point (center of the image)
        self.point_y = self.pos[1] + self.radius # visual center of point (center of the image)

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
        #include check for select mode? TODO
        if self.collide_point(*touch.pos):
            if touch.button == 'left':

                # Hold value of touch downed pos
                self.last_touch = touch.pos # Need this line
        return super(PointLayout, self).on_touch_down(touch)


    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                # move complete TODO: find some way to have figure update for this
                pass
        return super(PointLayout, self).on_touch_up(touch)


    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                self.x = self.x + touch.pos[0] - self.last_touch[0] # Add the x distance between this mouse event and the last
                self.y = self.y + touch.pos[1] - self.last_touch[1] # Add the y distance between this mouse event and the last
                self.point_x = self.pos[0] + self.radius
                self.point_y = self.pos[1] + self.radius
                self.last_touch = touch.pos # Update the last position of the mouse
        return super(PointLayout, self).on_touch_move(touch)
