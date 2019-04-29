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
from kivy.uix.switch import Switch
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.lang import Builder

from math import acos, degrees, atan2

from Point import *
from GeomMenuing import *
from Style import *


#big todos:
# maybe make point moving not try to detect collision during movement, just check that we're grabbed?


# point labels
    # coords?

# angle calculation should be in degrees, not radians
#fix(?) layout issues?
#buttons should hide if we haven't selected the appropriate number of points for them
    #maybe have cases in the operations themselves to prevent crashes
# possibly allow adding points by numeric input?

#removing points from figure?
#clearing all figures?




#list of ids for operation buttons
operations = ['distance_button','angle_button','area_button','perimeter_button','centroid_button','coords_button', 'deselect_all']

Builder.load_file('Geometry.kv')

class Geometry(FloatLayout):

    '''
    Sets all selected points to be unselected, and resets backend values to match
    '''
    def deselect_all(self):
        for selected in self.selected_points:
            selected.set_as_deselected()
        self.num_selected = 0
        self.selected_points = []
        self.select_event()

    '''
    Changes current mode of Geometry widget, performing book-keeping on backend values as needed
    '''
    def change_mode(self, mode):
        if (mode != 'adding') and (mode != 'selecting') and (mode != 'moving'):
            print("ERROR: Invalid move change attempted, this should never happen.")
            return False
        elif self.mode_state != mode: #don't change mode if the new mode is the same as the current mode (prevents accidental resets)
            if self.mode_state == "adding":
                #if we switch off of adding and there's a figure in process, we need to address it
                self.make_figure()

            if self.mode_state == "selecting":
                #if we switch off of selecting, deselect everything:
                self.deselect_all()

            self.mode_state = mode
            #resetting these just in case
            self.num_selected = 0
            self.in_prog_figure = None
            self.selected_points = []
            return True
        else:
            return False

    '''
    Completes figure by drawing a line for it, then resetting backend values
    '''
    def make_figure(self):
        if self.in_prog_figure is None:
            return False
        self.in_prog_figure.draw_fig()
        #set the in progress figure pointer back to None
        self.in_prog_figure = None
        self.num_adds = 0
        return True

    '''
    Cancels creation of current figure, removing all points from the incomplete figure and resetting backend values
    '''
    def cancel_figure(self):
        #don't try to cancel a figure creation with no actual points
        if self.in_prog_figure is None:
            return False
        self.in_prog_figure.clear_widgets()
        self.in_prog_figure = None
        self.num_adds = 0
        return True

    '''
    Used in processing touch events on the interactive space of Geometry. Some of this functionality is within the Points themselves.
    '''
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
                    self.num_adds+=1
                    self.in_prog_figure.add_point(contact_point[0], contact_point[1], self.num_adds)
                    self.add_event()
            else:
                #check if contact at point, if so continue
                if True:
                    if self.mode_state == 'selecting':
                        #REMOVE: handled within pointlayout
                        pass
                    elif self.mode_state == 'moving':
                        #REMOVE: handled within pointlayout
                        pass
                    else:
                        print("ERROR: Invalid mode_state interaction") #FIXME: remove if it turns out this never happens (it shouldn't)
                #otherwise, do nothing

    '''
    Used to alter visibility on make and cancel figure buttons based off how many points are present in the in_progress figure
    '''
    def add_event(self):
        if self.num_adds == 0:
            self.ids['make_figure_button'].hide_make()
            self.ids['cancel_figure_button'].hide_make()
        elif self.num_adds > 0:
            self.ids['make_figure_button'].hide_make(False)
            self.ids['cancel_figure_button'].hide_make(False)
        else:
            print("ERROR: Negative num_adds, this should never happen.")

    '''
    Used to alter visibility on operation buttons based off how many points are selected
    '''
    def select_event(self):
        #WARNING: make sure operations variable is up to date if using this function
        if self.num_selected == 0:
            self.hide_all_opps()
        elif self.num_selected == 1:
            self.hide_all_opps()
            self.ids['coords_button'].hide_opp(False)
            self.ids['deselect_all'].hide_opp(False)
        elif self.num_selected == 2:
            #only distance and centroid
            self.hide_all_opps()
            self.ids['deselect_all'].hide_opp(False)
            self.ids['distance_button'].hide_opp(False)
            self.ids['centroid_button'].hide_opp(False)
        elif self.num_selected == 3:
            #everything but coords
            self.hide_all_opps()
            self.ids['deselect_all'].hide_opp(False)
            self.ids['distance_button'].hide_opp(False)
            self.ids['centroid_button'].hide_opp(False)
            self.ids['angle_button'].hide_opp(False)
            self.ids['area_button'].hide_opp(False)
            self.ids['perimeter_button'].hide_opp(False)
        else:
            #everything but angles and coords
            self.hide_all_opps()
            self.ids['deselect_all'].hide_opp(False)
            self.ids['distance_button'].hide_opp(False)
            self.ids['centroid_button'].hide_opp(False)
            self.ids['area_button'].hide_opp(False)
            self.ids['perimeter_button'].hide_opp(False)

        # print(self.ids['angle_button'])
        pass

    '''
    Hides all operation buttons
    '''
    def hide_all_opps(self):
        #WARNING: make sure operations variable is up to date if using this function
        for opp in operations:
            self.ids[opp].hide_opp()


    '''
    Returns string for the coordinates of a single point.
    '''
    def calculateCoords(self):
        if self.num_selected != 1:
            return "More than/less than one point coordinates requested, this should never happen."
        point = self.selected_points[0]
        result = "Coordinates of " + str(point.p.get_lab()) + " : (" + str('%.3f'%point.v_point_x) + ", " + str('%.3f'%point.v_point_y) + ")"
        return result


    def __centerOf__(self):
        if self.selected_points is None:
            return [0.0,0.0]
        sum_x = 0.0
        sum_y = 0.0
        n = len(self.selected_points)
        for i in range(0, n):
            sum_x += self.selected_points[i].v_point_x
            sum_y += self.selected_points[i].v_point_y
        center = ((float(sum_x)/n), (float(sum_y)/n))
        return center

    # def __ccwCompare__(self,center):
    #     a1 = (degrees(atan2(a.v_point_x - center[0], a.v_point_y - center[1])) + 360) % 360
    #     a2 = (degrees(atan2(b.v_point_x - center[0], b.v_point_y - center[1])) + 360) % 360
    #     return int(a1-a2)

    def __ccwCompare__(self, center):
        for i, p in enumerate(self.selected_points):
            if i+2 > len(self.selected_points): break
            a = self.selected_points[i]
            b = self.selected_points[i+1]
            a1 = (degrees(atan2(a.v_point_x - center[0], a.v_point_y - center[1])) + 360) % 360
            a2 = (degrees(atan2(b.v_point_x - center[0], b.v_point_y - center[1])) + 360) % 360
            a.compare = int(a1-a2)

    def __sortCCW__(self):
        center = self.__centerOf__()
        self.__ccwCompare__(center)
        ccw = sorted(self.selected_points, key=lambda x: x.compare)
        return ccw

    '''
    Returns string of the area of a series of points, treating them as a polygon
    '''
    #FIXME: calculation is sometimes negative, needs points to be listed counterclockwise
    def calculateArea(self):
        if self.selected_points is None:
            return 0.0
        # Based off of dszarkow's implementation of the Surveyor's Formula on codeproject.
        # Available at: https://www.codeproject.com/Articles/13467/A-JavaScript-Implementation-of-the-Surveyor-s-Form
        area = 0.0
        result = "Area of "
        ccw = self.__sortCCW__()
        for i, p in enumerate(ccw): #for all points, enumerated as indices i
            result += str(ccw[i].p.get_lab()) + ", "
            print(ccw[i].p.get_lab())
            if i+2 > len(ccw): break
            x_diff = ccw[i+1].v_point_x - ccw[i].v_point_x
            y_diff = ccw[i+1].v_point_y - ccw[i].v_point_y
            area += ccw[i].v_point_x * y_diff - ccw[i].v_point_y * x_diff

        area = '%.3f'%(area*.5)
        result+= "= " + str(area)
        return result
    '''
    Returns string of the perimeter of a series of points, treating them as a polygon
    '''
    #FIXME: calculation needs points to be listed counterclockwise
    def calculatePerimeter(self):
        if self.selected_points is None:
            return 0.0
        # Based off of dszarkow's implementation of the Surveyor's Formula on codeproject.
        # Available at: https://www.codeproject.com/Articles/13467/A-JavaScript-Implementation-of-the-Surveyor-s-Form
        perimeter = 0.0
        result = "Perimeter of "
        for i, p in enumerate(self.selected_points): #for all points, enumerated as indices i
            result += str(self.selected_points[i].p.get_lab()) + ", "
            if i+2 > len(self.selected_points): break
            x_diff = self.selected_points[i+1].v_point_x - self.selected_points[i].v_point_x
            y_diff = self.selected_points[i+1].v_point_y - self.selected_points[i].v_point_y
            perimeter += perimeter + (x_diff * x_diff + y_diff * y_diff)**0.5
        result+= '%.3f'%(perimeter)
        return result

    '''
    Returns string of the dstance of a series of points in the order they were selected
    '''
    def calculateDistance(self):
        if self.selected_points is None:
            return 0.0
        distance = 0.0
        result = "Distance of " + str(self.selected_points[0].p.get_lab()) + ", "
        for i in range(1, len(self.selected_points)):
            x_diff = self.selected_points[i].v_point_x - self.selected_points[i-1].v_point_x
            y_diff = self.selected_points[i].v_point_y - self.selected_points[i-1].v_point_y
            distance+= (x_diff**2 + y_diff**2)**.5
            result += str(self.selected_points[i].p.get_lab())+", "
        distance = '%.3f'%(distance)
        result+= "= " + str(distance)
        return result

    '''
    Returns string of the centroid of a series of points
    '''
    def calculateCentroid(self):
        if self.selected_points is None:
            return [0.0,0.0]
        sum_x = 0.0
        sum_y = 0.0
        n = len(self.selected_points)
        result = "Centroid of "
        for i in range(0, n):
            sum_x += self.selected_points[i].v_point_x
            sum_y += self.selected_points[i].v_point_y
            result+= str(self.selected_points[i].p.get_lab())+", "
        centroid = ('%.3f'%(float(sum_x)/n), '%.3f'%(float(sum_y)/n))
        result += "= " + str(centroid)
        return result

    '''
    Returns string of the angle formed by 3 points, with the second selected point as the vertex
    '''
    def calculateAngle(self):
        if(self.num_selected > 3):
            return "ERROR: More than 3 points selected, this should never happen"
        a = self.selected_points[0]
        v = self.selected_points[1] #vertex
        b = self.selected_points[2]
        #construct string without value
        result = "Angle of " + str(a.p.get_lab()) + ", " + str(v.p.get_lab()) + ", " + str(b.p.get_lab()) + "= "

        #distance between vertex and each point, and those points themselves
        ab = ((b.v_point_x - a.v_point_x)**2 + (b.v_point_y - a.v_point_y)**2)**.5
        va = ((v.v_point_x - a.v_point_x)**2 + (v.v_point_y - a.v_point_y)**2)**.5
        vb = ((v.v_point_x - b.v_point_x)**2 + (v.v_point_y - b.v_point_y)**2)**.5

        angle = acos((va**2 + vb**2 - ab**2) / (2 * va * vb))
        angle = '%.3f'%(degrees(angle))
        result += str(angle)
        return result

    def Save(self):
        figures = []
        for i in self.interactive_space.children:
            points = []
            for j in i.children:
                points.append(j.pos)
            figures.append(points)
        return figures

    def Load(self, bringItBack):
        print(bringItBack)
        for i in bringItBack:
            print(i)
            f = Figure()
            self.in_prog_figure = f
            self.interactive_space.add_widget(self.in_prog_figure)
            for j in i:
                self.in_prog_figure.add_point(j[0], j[1])
            self.make_figure()
        print(len(self.children))



    def __init__(self, *args, **kwargs):
        super(Geometry, self).__init__(*args, **kwargs)
        self.size_hint = .7,.7

        #the different modes the user can be in within the geometry app, defaults to adding
        self.mode_state = 'adding' #for some reason i can't get OptionProperty to behave correctly here, despite this being exactly the kind of situation you use it in.
        self.num_selected = 0 #number of points selected within select mode, not using NumericProperty for similar reasons as above
        self.selected_points = []
        self.num_adds = 0

        # self.interactive_space = None
        self.in_prog_figure = None #If we're in the middle of making a figure, this points to that in some way


class Interactive_Space(FloatLayout): #class used to describe space containing points
    pass

class Result(Label):
    def update_result(self, new_result):
        self.text = str(new_result)
        return True













"""
    A Figure contains a series of points that make up the shape they are meant to form. This can be a fully closed polygon, line segment, or point.
"""
class Figure(Widget):

    # def draw_line(self):
    def draw_fig(self):
        #traverse points to draw line of figure
        coords = []

        for p in self.children:
            coords.append(p.a_point_x)
            coords.append(p.a_point_y)

        self.canvas.remove(self.line_draw)
        new_line = InstructionGroup()
        new_line.add(Color(rose_50[0], rose_50[1], rose_50[2], rose_50[3], mode='rgba'))
        new_line.add(Line(points=coords, close=True, width=2))
        self.line_draw = new_line
        self.canvas.add(self.line_draw)
        return

    def add_point(self, new_x, new_y, new_lab):
        p = PointLayout(pos=[new_x-(img_size[0]/2), new_y-(img_size[0]/2)])
        self.add_widget(p)
        p.set_relative_pos()
        p.set_lab(new_lab)


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
