from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Line, Color, InstructionGroup
from kivy.uix.widget import Widget


class MyWidget(Widget):

    undolist = []
    objects = []
    drawing = False
    eraser = False;

    def on_touch_up(self, touch):
        self.drawing = False

    def on_touch_move(self, touch):
        if self.eraser == False:
            if self.drawing:
                self.points.append(touch.pos)
                self.obj.children[-1].points = self.points
            else:
                self.drawing = True
                self.points = [touch.pos]
                print(self.points)
                self.obj = InstructionGroup()
                self.obj.add(Color(0,0,0))
                self.obj.add(Line(width = 2.5))
                self.objects.append(self.obj)
                self.canvas.add(self.obj)
        else:
            for obj in self.objects:
                for point in obj.children[-1].points:
#                    if point.
                    templine = Line(width = 2.5, points = [touch.pos])
                    if point == (templine.points[0],templine.points[1]):
                        print(obj.children[-1].points)
                        self.canvas.remove(obj)
                        obj.children[-1].points.remove(point)
                        print(obj.children[-1].points)
                        self.canvas.add(obj)

    def toggleEraser(self):
        if self.eraser == False:
            print("Eraser on")
            self.eraser = True
        else:
            print("Eraser off")
            self.eraser = False

    def undo(self):
        item = self.objects.pop(-1)
        self.undolist.append(item)
        self.canvas.remove(item)

    def redo(self):
        item = self.undolist.pop(-1)
        self.objects.append(item)
        self.canvas.add(item)


KV = """

BoxLayout:
    MyWidget:
        id: widget
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "blank-notebook-paper-template.jpg"
    Button:
        text: "toggleEraser"
        on_release:
            widget.toggleEraser()
    Button:
        text: "redo"
        on_release:
            widget.redo()


"""


class MyApp(App):

    def build(self):
        root = Builder.load_string(KV)
        return root

MyApp().run()
