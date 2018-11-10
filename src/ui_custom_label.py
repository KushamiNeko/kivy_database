from kivy.uix.label import Label
from kivy.lang import Builder


from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty

from ui_setting import SettingMainUI
#from ui_setting import SettingCustomLabel

Builder.load_string("""
<CustomLabel>:
  canvas.before:
    Color:
      rgba: self.bg_color

    Rectangle:
      pos: self.pos
      size: self.size
""")

class CustomLabel(Label):
    
    bg_color = ListProperty(SettingMainUI.default_color_grey)

    def __init__(self, bg_color=None, **kargs):

        if bg_color:
            self.bg_color = bg_color

        super(CustomLabel, self).__init__(**kargs)

#    def __init__(self, bg_color=None, **kargs):
#
#        super(CustomLabel, self).__init__(**kargs)
#
#        self.font_size = MainUISetting.main_font_size
#
#        with self.canvas.before:
#            self.bind(size=self.update_rect, pos=self.update_rect)
#
#        if bg_color:
#            self.bg_color = bg_color
#        else:
#            self.bg_color = MainUISetting.custom_label_default_color
#
#    def update_rect(self, instance, value):
#        self.rect.pos = instance.pos
#        self.rect.size = instance.size
#
#    @property
#    def bg_color(self):
#        return self._bg_color
#
#    @bg_color.setter
#    def bg_color(self, bg_color):
#        self._bg_color = bg_color
#
#        with self.canvas.before:
#            self.color = Color(*self._bg_color).rgba
#
#            self.rect = Rectangle(size=self.size,
#                                  pos=self.pos)
#
#        self.color = Color(1, 1, 1, 1).rgba


