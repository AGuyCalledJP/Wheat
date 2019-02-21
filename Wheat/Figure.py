from enum import Enum
#gonna need a whole load of imports to make this

class Point_State(Enum):
    UNSELECTED = 0
    SELECTED = 1

class Figure(Widget):
    def draw_points(self):
        # traverse points and draw each one in figure
        for p in self.points:
            #draw point at p
        return

    def draw_line(self):
        #traverse points to draw line of figure
        return

    # TODO: add content
    def __init__(self, points):
        # TODO: ASSERTIONS FOR VALID PARAMETERS
        self.points = points
        self.draw_line()
        self.draw_points()



class FigPoint(Widget):
    # TODO: add content
    def __init__(self, label, x, y, state=Point_State.UNSELECTED):
        # TODO: ASSERTIONS FOR VALID PARAMETERS
        self.label = label
        self.x = x
        self.y = y
