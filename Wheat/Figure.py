#FILE UNFINISHED, DO NOT USE

"""
    Figure contains class structures for FigPoints, and Figures, which are collections of FigPoints with visual display functions.
    Both are widgets.
"""
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.floatlayout import FloatLayout
from enum import Enum
#gonna need a whole load of imports to make this

"""
    PointState is used to determine if a point has been selected or not, for use in operations performed on figures.
"""
class PointState(Enum):
    UNSELECTED = 0
    SELECTED = 1


POINT_RAD = 10.



class VisualLayout(ScatterLayout):
    #GOTTA ADD SOME STUFF HERE
    pass

class FigureLayout(VisualLayout):
    #GOTTA ADD SOME STUFF HERE
    pass








"""
    A Figure contains a series of points that make up the shape they are meant to form. This can be a fully closed polygon, line segment, or point.
"""
class Figure(Widget):
    def draw_points(self):
        # traverse points and draw each one in figure
        for p in self.points:
            #draw point at p
            with self.canvas:
                Color(1,1,0) # YELLOW
                d = 2*(POINT_RAD + 1.) #outer boundary
                Ellipse(pos= ((p.x - d/2), (p.y - d/2)), size= (d,d) )

                Color(0,1,0) # RED
                d = 2*POINT_RAD
                Ellipse(pos= ((p.x - d/2), (p.y - d/2)), size= (d,d) )

                #TODO: Draw label on or around point?
        return

    def draw_line(self):
        #traverse points to draw line of figure
        coords = []

        for p in self.points:
            coords.append(p.x)
            coords.append(p.y)

        with self.canvas:
            Color(1,1,1) #WHITE
            Line(coords)
        return

    def draw_fig(self):
        if(self.canvas):
            self.canvas.clear() #remove all previous points and lines on this figure (this hopefully only effects one figure?)
        self.draw_line()
        self.draw_points()
        return


    def calculateArea(self):
        # Based off of dszarkow's implementation of the Surveyor's Formula on codeproject.
        # Available at: https://www.codeproject.com/Articles/13467/A-JavaScript-Implementation-of-the-Surveyor-s-Form
        area = 0.0
        for i, p in enumerate(self.points): #for all points, enumerated as indices i
            x_diff = self.points[i+1].x - self.points[i].x
            x_diff = self.points[i+1].y - self.points[i].y
            area += self.points[i].x * y_diff - self.points[i].y * x_diff
        return 0.5 * area

    def calculatePerimeter(self):
        # Based off of dszarkow's implementation of the Surveyor's Formula on codeproject.
        # Available at: https://www.codeproject.com/Articles/13467/A-JavaScript-Implementation-of-the-Surveyor-s-Form
        perimeter = 0.0
        for i, p in enumerate(self.points): #for all points, enumerated as indices i
            x_diff = self.points[i+1].x - self.points[i].x
            x_diff = self.points[i+1].y - self.points[i].y
            perimeter += perimeter + (x_diff * x_diff + y_diff * y_diff)**0.5
        return perimeter

    # TODO: add content
    def __init__(self, points):
        # TODO: ASSERTIONS FOR VALID PARAMETERS
        self.points = points
        self.draw_fig()



"""
    Ellipses are drawn differently than figures (since we're drawing about a point, rather than along a series of points), leading to different logic behind the class.
"""

#TODO: Maybe find a way to put these under the same class.
class FigEllipse(Widget):
    def draw_fig(self):
        pass

    def __init__(self, xcenter, ycenter, xrad, yrad):
        # TODO: ASSERTIONS FOR VALID PARAMETERS
        self.xcenter = xcenter
        self.ycenter = ycenter
        self.xrad = xrad
        self.yrad = yrad
        # self.marked = False #TODO: may remove, indicator for if there are points/lines marked on figure

        # add bounding box in shape of a circle?







"""
    A FigPoint is a widget used in the formation of Figures. It has an x-y position, a label, and a state.
"""
class FigPoint(Widget):
    # TODO: maybe use their pos tuple thing??
    def __init__(self, label, x, y, state=PointState.UNSELECTED):
        # TODO: ASSERTIONS FOR VALID PARAMETERS
        self.label = label
        self.x = x
        self.y = y

    def collide_point(self,x,y): # override of existing
        if( ((self.x - x)**2 + (self.y - y)**2) == POINT_RAD**2): #if the distance between the given point and this point is less than the radius of the visual circle around the point, we have collision
            return True
        else:
            return False

#ideas: inherit from rectangle and ellipse?


class FigApp(App):
    def build(self):
        f = FloatLayout()
        v = VisualLayout(do_rotation=False, size=(200,200), size_hint=(None, None), pos=(10, 10))
        f.add_widget(v)
        pointA = FigPoint(label="A", x=20, y=20)
        pointB = FigPoint(label="B", x=30, y=60)
        fig = Figure([pointA, pointB])
        v.add_widget(fig)

        return f

FigApp().run()
