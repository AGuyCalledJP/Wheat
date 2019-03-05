from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class PointButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PointButton, self).__init__(**kwargs)
        self.source = 'visual_assets/fig_point.png'
        self.selected = False

    def on_press(self):
        if(self.selected == False):
            self.source = 'visual_assets/fig_point_selected.png'
            self.selected = True
        else:
            self.source = 'visual_assets/fig_point.png'
            self.selected = True



class SampleApp(App):
    def build(self):
        return PointButton()


SampleApp().run()
