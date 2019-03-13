from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('draw.kv')

class Draw(BoxLayout):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(0,0,0)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width = 2.5)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x,touch.y]
