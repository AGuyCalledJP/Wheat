from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import Ellipse
from kivy.graphics import Line
from kivy.graphics import InstructionGroup

from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.lang import Builder

import re

from Point import *

class RightPane(FloatLayout):
    '''
    Hides right pane of geometry menu.
    '''
    def hide_pane(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
                return 1 #return values indicate size the header should be in th kv file, which runs this and sets header's size_hint to this value
        #capture sizing information, opacity, disabled status, and set to 0's/None/True to hide the pane
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True
            return .66 #return values indicate size the header should be in th kv file, which runs this and sets header's size_hint to this value





class OppButton(Button):
    '''
    Hides operation button.
    '''
    def hide_opp(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        #capture sizing information, opacity, disabled status, and set to 0's/None/True to hide the pane
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

    def __init__(self, **kwargs):
        super(OppButton, self).__init__(**kwargs)
        self.hide_opp() #start hidden



class MakeFigureButton(Button):
    '''
    Hides make operation button.
    '''
    def hide_make(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        #capture sizing information, opacity, disabled status, and set to 0's/None/True to hide the pane
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

    def __init__(self, **kwargs):
        super(MakeFigureButton, self).__init__(**kwargs)
        self.hide_make() #start hidden, use when we have add functionality working


class ManualEntryLayout(GridLayout):
    '''
    Hides container for manual point input.
    '''
    def hide_entry(wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        #capture sizing information, opacity, disabled status, and set to 0's/None/True to hide the pane
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    '''
    Filters text input to accept only numbers and a single decimal point.
    '''
    def insert_text(self, substring, from_undo=False, multiline = False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)
