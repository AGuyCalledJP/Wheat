
from kivy.graphics import Color, Ellipse, Line, Rectangle, InstructionGroup
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('draw.kv')

class Draw(BoxLayout):
    pass

class Paint(Widget):
    undolist = []
    objects = []
    drawing = False

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
                self.obj.add(Color(0,0,0))
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
                print('help!')
                self.undo()
#        self.objects = []
#        self.canvas.clear()
