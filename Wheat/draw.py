import shutil, os
from kivy.graphics import Color, Ellipse, Line, Rectangle, InstructionGroup
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty, NumericProperty,
                             OptionProperty, BooleanProperty,
                             StringProperty, ListProperty)
import copy
from shutil import copy2
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window


write = JsonStore('Notebook/PageState/writing.json')

Builder.load_file('draw.kv')

f = "page"
suffix = ".png"
newPage = "visual_assets/wheat_bg_1_college.png"
newGraphPage = "visual_assets/wheat_bg_1.png"
folder = '/Notebook/Pages/'
color = 'black'
sz = 2.5

class Draw(BoxLayout):

    pages = []
    count = 0
    curr = 0
    pt = None

    def __init__(self, *args, **kwargs):
        super(Draw, self).__init__(*args, **kwargs)
        cd = os.getcwd()
        pages = os.listdir(cd + folder)
        pages.sort()
        if self.pt is None:
            self.pt = 1
        if len(pages) > 0:
            for page in pages:
                self.p = Paint(cd + folder + page, self.pt)
                self.pages.append(self.p)
                self.count = self.count + 1
            self.add_widget(self.pages[0])
        else:
            if self.pt is 1:
                self.p = Paint(newPage, self.pt)
            else:
                self.p = Paint(newGraphPage, self.pt)
            self.count += 1
            self.pages.append(self.p)
            self.add_widget(self.p)
        self.Load()

    def Save(self):
        sz = Window.size
        cwd = os.getcwd()
        i = self.pages[self.curr]
        if i.myPt is 1:
            src = cwd + "/Wheat/" + newPage
        else:
            src = cwd + "/Wheat/" + newGraphPage
        dest = cwd + folder + f + str(self.curr) + suffix
        exists = os.path.isfile(dest)
        if not exists:
            copy2(src, dest)
        writing = i.Save()
        currsz = []
        currsz.append(sz[0])
        currsz.append(sz[1])
        save = "P" + str(self.curr)
        write.put(save, writing = writing[0], color = writing[1], width = writing[2], sz = currsz)

    def Load(self):
        sz = Window.size
        p = 'P' + str(self.curr)
        curr = None
        color = None
        width = None
        scale = None
        found = False
        for key in write.keys():
            if p in key:
                found = True
                written = write.get(p)
                curr = copy.deepcopy(written['writing'])
                color = copy.deepcopy(written['color'])
                width = copy.deepcopy(written['width'])
                scale = written['sz']
        if found:
            xl = scale[0]
            xc = sz[0]
            yl = scale[1]
            yc = sz[1]
            xfactor = float(xc/xl)
            yfactor = float(yc/yl)
            for i in curr:
                for j in i:
                    j[0] = j[0] * xfactor
                    j[1] = j[1] * yfactor
            page = self.pages[self.curr]
            page.Load(curr, color, width)


    def pageBack(self):
        if self.curr > 0:
            self.Save()
            oldP = self.pages[self.curr]
            self.remove_widget(oldP)
            self.curr = self.curr - 1
            newP = self.pages[self.curr]
            self.add_widget(newP)
            oldP.update()
            newP.update()
            self.Load()

    def pageForward(self):
        if self.curr == self.count - 1:
            self.Save()
            oldP = self.pages[self.curr]
            oldP.rem()
            self.remove_widget(oldP)
            if self.pt is 1:
                newP = Paint(newPage, self.pt)
            else:
                newP = Paint(newGraphPage, self.pt)
            self.pages.append(newP)
            self.add_widget(newP)
            oldP.update()
            newP.update()
            self.curr = self.curr + 1
            self.count = self.count + 1
        else:
            self.Save()
            oldP = self.pages[self.curr]
            oldP.rem()
            self.remove_widget(oldP)
            self.curr = self.curr + 1
            newP = self.pages[self.curr]
            self.add_widget(newP)
            oldP.update()
            newP.update()
            self.Load()
        with self.canvas:
            self.canvas.ask_update()

    def undo(self):
        self.pages[self.curr].undo()

    def redo(self):
        self.pages[self.curr].redo()

    def clear_canvas(self):
        self.pages[self.curr].clear_canvas()

    def chColor(self, col):
        # global color
        # if color == 'black':
        #     color = 'red'
        # else:
        #     color = 'black'
        global color
        color = col

    def getColor(self):
        global color
        return color

    def increaseSize(self):
        global sz
        sz = sz + .25

    def decreaseSize(self):
        global sz
        if sz > .1:
            sz = sz - .25

    def getSize(self):
        global sz
        return sz

    def pageType(self):
        if self.pt is 1:
            self.pt = 2
        else:
            self.pt = 1

class Paint(Widget):
    objects = None
    beenThere = None
    colCurr = None
    widCurr = None
    undolist = None
    doneThat = None
    colUndo = None
    widUndo = None
    points = None
    drawing = False
    myPt = None

    def __init__(self, where, myPt, *args, **kwargs):
        super(Paint, self).__init__(*args, **kwargs)
        if self.objects is None:
            self.objects = []
            self.beenThere = []
            self.colCurr = []
            self.widCurr = []
            self.undolist = []
            self.doneThat = []
            self.colUndo = []
            self.widUndo = []
            self.points = []
            self.myPt = myPt
        with self.canvas:
                self.bg = Rectangle(source=where, pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def rem(self):
        self.parent.remove_widget(self)

    def update(self):
        with self.canvas:
            self.canvas.ask_update()

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_touch_up(self, touch):
        self.drawing = False

    def on_touch_move(self, touch):
        global sz
        global color
        if self.collide_point(touch.x, touch.y):
            if self.drawing:
                self.points.append([touch.x, touch.y])
                self.obj.children[-1].points = self.points
            else:
                self.drawing = True
                self.points = [[touch.x, touch.y]]
                self.obj = InstructionGroup()
                if color == 'black':
                    self.obj.add(Color(0,0,0))
                else:
                    self.obj.add(Color(1,.4,.4))
                L = Line(width = sz)
                self.obj.add(L)
                self.objects.append(self.obj)
                self.beenThere.append(self.points)
                self.colCurr.append(color)
                self.widCurr.append(sz)
                self.canvas.add(self.obj)

    def redrawLine(self, bundle, color, width):
        coords = []

        for b in bundle:
            coords.append(b[0])
            coords.append(b[1])

        self.obj = InstructionGroup()
        if color == 'black':
            self.obj.add(Color(0,0,0))
        else:
            self.obj.add(Color(1,.4,.4))
        self.obj.add(Line(points=coords, width = width))
        line_draw = self.obj
        self.objects.append(self.obj)
        self.beenThere.append(bundle)
        self.colCurr.append(color)
        self.widCurr.append(width)
        self.canvas.add(line_draw)

    def undo(self):
        if len(self.objects) > 0:
            item = self.objects.pop(-1)
            luggage = self.beenThere.pop(-1)
            col = self.colCurr.pop(-1)
            wid = self.widCurr.pop(-1)
            self.undolist.append(item)
            self.doneThat.append(luggage)
            self.colUndo.append(col)
            self.widUndo.append(wid)
            self.canvas.remove(item)

    def redo(self):
        if len(self.undolist) > 0:
            item = self.undolist.pop(-1)
            luggage = self.doneThat.pop(-1)
            col = self.colUndo.pop(-1)
            wid = self.widUndo.pop(-1)
            self.objects.append(item)
            self.beenThere.append(luggage)
            self.colCurr.append(col)
            self.widCurr.append(wid)
            self.canvas.add(item)

    def clear_canvas(self):
        if len(self.objects) > 0:
            for i in range(len(self.objects)):
                self.undo()

    def Save(self):
        curr = copy.deepcopy(self.beenThere)
        color = copy.deepcopy(self.colCurr)
        width = copy.deepcopy(self.widCurr)
        return [curr, color, width]

    def Load(self, writing, color, width):
        self.clear_canvas()
        one = len(writing)
        two = len(color)
        three = len(width)
        if one is two and one is three and two is three:
            for i in range(0, len(writing)):
                self.redrawLine(writing[i], color[i], width[i])
        else:
            print("something went wrong here sorry")

class StrokeLabel(Label):

    def __init__(self, *args, **kwargs):
        super(StrokeLabel, self).__init__(*args, **kwargs)
        self.text = "Stroke: " + str(2.5)

    def update_stroke_label(self, new_size):
        self.text = "Stroke: " + str(new_size)
