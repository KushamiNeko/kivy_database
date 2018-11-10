from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from kivy.uix.behaviors import FocusBehavior

from kivy.graphics import Color, Rectangle

import pymongo
from mongo_interface import MongoInterface


#import ui_setting as UISetting
from ui_setting import SettingMainUI
import ui_custom_label as UICustomLabel


class FocusWithColor(FocusBehavior):

    def __init__(self, **kargs):
        super(FocusWithColor, self).__init__(**kargs)

        with self.canvas:
            self.color = Color(1, 1, 1, 0.0)
            self.rect = Rectangle(size=self.size,
                                  pos=self.pos)

            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_focus(self, instance, value, *largs):
        if value:
            self.color.rgba = SettingMainUI.data_row_selected_color
        else:
            self.color.rgba = (0.0, 0.0, 0.0, 0.0)


class DataArea(ScrollView):

    def __init__(self, top_window, parent_container,
                 categories, datas, **kargs):

        self.top_window = top_window
        self.parent_container = parent_container
        self.categories = categories
        self.datas = datas

        self.categories_row = None
        self.data_rows = []

        super(DataArea, self).__init__(**kargs)

        self.do_scroll_y = False
        self.size_hint = (1, 1)

        self.data_area_container = BoxLayout(
            orientation='vertical',
            spacing=SettingMainUI.main_spacing)

        self.add_widget(self.data_area_container)

        self.update_widget()

        print(self.datas)

    def update_widget(self):

        if self.categories_row:
            self.data_area_container.remove_widget(self.categories_row)

        if self.data_rows:
            for i in self.data_rows:
                self.data_area_container.remove_widget(i)

        self.categories_row = CategoriesRow(self.top_window, self.data_area_container,
                                            self.categories, self.datas)

        self.categories_row.update_widget()

        self.data_area_container.add_widget(self.categories_row)

        for i in range(SettingMainUI.data_area_rows_per_page):
            data_row = DataRow(self.top_window, self.data_area_container,
                               self.categories, self.datas)

            data_row.update_widget()

            self.data_area_container.add_widget(data_row)

            self.data_rows.append(data_row)

    def update_data(self):
        pass


class CategoriesRow(BoxLayout):

    def __init__(self, top_window, parent_container,
                 categories, datas, **kargs):

        self.top_window = top_window
        self.parent_container = parent_container

        self.categories = categories
        self.datas = datas

        self.categories_content = []

        super(CategoriesRow, self).__init__(**kargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, 1)
        self.spacing = SettingMainUI.main_spacing

    def update_widget(self):
        for j in range(0, len(self.categories)):
            label = UICustomLabel.CustomLabel(
                text='',
                font_size=SettingMainUI.main_font_size,
                bg_color=SettingMainUI.categories_row_color)

            self.add_widget(label)
            self.categories_content.append(label)


class DataRow(FocusWithColor, BoxLayout):

    def __init__(self, top_window, parent_container,
                 categories, datas, **kargs):

        self.top_window = top_window
        self.parent_container = parent_container

        self.categories = categories
        self.datas = datas

        self.data_content = []

        super(DataRow, self).__init__(**kargs)

        self.orientation = 'horizontal'
        self.size_hint = (1, 1)
        self.spacing = SettingMainUI.main_spacing

    def update_widget(self):

        for j in range(0, len(self.categories)):
            label = UICustomLabel.CustomLabel(
                text='',
                font_size=SettingMainUI.main_font_size)

            self.add_widget(label)
            self.data_content.append(label)

    def update_data(self):
        pass

        #    if datas:
        #        try:
        #            data = datas[categories[j]]

        #            if data:
        #                text = data
        #            else:
        #                text = ''

        #        except (IndexError, KeyError):
        #            text = ''

        #        label = CustomLabel(text=text)

        #    else:
        #        label = CustomLabel(text='')

        #    self.add_widget(label)
        #    self.data_labels.append(label)

        # parent.add_widget(self)

#    def set_data(self, categories, datas):
#
#        self.categories = categories
#        self.datas = datas
#
#        for j in range(0, len(categories)):
#
#            text = ''
#
#            if datas:
#                try:
#                    data = datas[categories[j]]
#                    print(data)
#
#                    if data:
#                        text = data
#
#                except (IndexError, KeyError):
#                    pass
#
#            self.data_labels[j].text = text
#
#        #self.data_labels[0].text = text
#        # print(self.data_labels)
#        # print(len(self.data_labels))

    def on_focused(self, instance, value, *largs):

        if value:
            self.top_window.data_row_focused = instance

        for i in self.data_content:
            if value:
                i.bg_color = self.color.rgba
            else:
                i.bg_color = SettingMainUI.custom_label_default_color
