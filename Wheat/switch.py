from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty


class Switch(Widget):
    '''Switch class. See module documentation for more information.
    '''
    active = BooleanProperty(False)
    '''Indicate whether the switch is active or inactive.

    :attr:`active` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to False.
    '''

    touch_control = ObjectProperty(None, allownone=True)
    '''(internal) Contains the touch that currently interacts with the switch.

    :attr:`touch_control` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to None.
    '''

    touch_distance = NumericProperty(0)
    '''(internal) Contains the distance between the initial position of the
    touch and the current position to determine if the swipe is from the left
    or right.

    :attr:`touch_distance` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0.
    '''

    active_norm_pos = NumericProperty(0)
    '''(internal) Contains the normalized position of the movable element
    inside the switch, in the 0-1 range.

    :attr:`active_norm_pos` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0.
    '''

    def on_touch_down(self, touch):
        if self.disabled or self.touch_control is not None:
            return
        if not self.collide_point(*touch.pos):
            return
        touch.grab(self)
        print(self.active)
        self.touch_distance = 0
        self.touch_control = touch
        return True


    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        self.touch_distance = touch.x - touch.ox
        return True


    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        # depending of the distance, activate by norm pos or invert
        if abs(touch.ox - touch.x) < 5:
            self.active = not self.active
        else:
            self.active = self.active_norm_pos > 0.5
        Animation(active_norm_pos=int(self.active), t='out_quad',
                  d=.2).start(self)
        self.touch_control = None
        return True



if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(Switch())
