import shutil, os
from kivy.graphics import Color, Ellipse, Line, Rectangle, InstructionGroup
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty, NumericProperty,
                             OptionProperty, BooleanProperty,
                             StringProperty, ListProperty)

Builder.load_file('draw.kv')

f = "page"
suffix = ".png"
newPage = "visual_assets/wheat_bg_1_college.png"
folder = '/Wheat/Notebook/Pages/'

class Draw(BoxLayout):

    pages = []
    count = 0
    curr = 0

    def __init__(self, *args, **kwargs):
        super(Draw, self).__init__(*args, **kwargs)
        cd = os.getcwd()
        pages = os.listdir(cd + folder)
        pages.sort()
        if len(pages) > 0:
            for page in pages:
                print(page)
                p = Paint(cd + folder + page)
                self.pages.append(p)
                print(self.pages)
                self.count = self.count + 1
            self.add_widget(self.pages[0])
        else:
            p = Paint(newPage)
            self.pages.append(p)
            self.add_widget(p)
            print(self.pages)

    def Save(self):
        print("hello there")
        files = []
        cd = os.getcwd()
        print(cd)
        for i in range(0,len(self.pages)):
            files.append(self.pages[i].Save(i))
        for f in files:
            if os.path.isfile(cd + folder + f):
                os.remove(cd + folder + f)
            shutil.move(f, str(cd + folder))
    def Load(self):
        pass
        

    def pageBack(self):
        if self.curr > 0:
            oldP = self.pages[self.curr]
            self.remove_widget(oldP)
            #oldP.rem()
            self.curr = self.curr - 1
            newP = self.pages[self.curr]
            self.add_widget(newP)
            oldP.update()
            newP.update()

    
    def pageForward(self):
        if self.curr == self.count - 1:
            print(self.curr)
            oldP = self.pages[self.curr]
            print(oldP)
            oldP.rem()
            self.remove_widget(oldP)
            newP = Paint(newPage)
            self.pages.append(newP)
            print(self.pages)
            self.add_widget(newP)
            oldP.update()
            newP.update()
            self.curr = self.curr + 1
            self.count = self.count + 1
        else:
            oldP = self.pages[self.curr]
            oldP.rem()
            self.remove_widget(oldP)
            self.curr = self.curr + 1
            newP = self.pages[self.curr]
            self.add_widget(newP)
            oldP.update()
            newP.update()
        with self.canvas:
            self.canvas.ask_update()



    def undo(self):
        self.pages[self.curr].undo()

    def redo(self):
        self.pages[self.curr].redo()

    def chColor(self):
        self.pages[self.curr].chColor()

    def clear_canvas(self):
        self.pages[self.curr].clear_canvas()

class Paint(Widget):
    undolist = []
    objects = []
    drawing = False
    color = 'black'

    def __init__(self, where, *args, **kwargs):
        super(Paint, self).__init__(*args, **kwargs)
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
        if self.collide_point(touch.x, touch.y):
            if self.drawing:
                self.points.append(touch.pos)
                self.obj.children[-1].points = self.points
            else:
                self.drawing = True
                self.points = [touch.pos]
                self.obj = InstructionGroup()
                if self.color == 'black':
                    self.obj.add(Color(0,0,0))
                else:
                    self.obj.add(Color(1,.4,.4))
                self.obj.add(Line(width = 2.5))
                self.objects.append(self.obj)
                self.canvas.add(self.obj)


    def undo(self):
        if len(self.objects) > 0:
            item = self.objects.pop(-1)
            self.undolist.append(item)
            self.canvas.remove(item)

    def redo(self):
        if len(self.undolist) > 0:
            item = self.undolist.pop(-1)
            self.objects.append(item)
            self.canvas.add(item)

    def clear_canvas(self):
        if len(self.objects) > 0:
            print(len(self.objects))
            for i in range(len(self.objects)):
                self.undo()
#        self.objects = []
#        self.canvas.clear()

    def chColor(self):
        if self.color == 'black':
            self.color = 'red'
        else:
            self.color = 'black'

    def Save(self, who):
        print("hello there")
        self.export_to_png(str(f + str(who) + suffix))
        return str(f + str(who) + suffix)
