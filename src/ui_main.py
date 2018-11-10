import gi

gi.require_version('Gtk', '3.0')

import kivy

from kivy.config import Config
kivy.require('1.9.1')

Config.set('kivy', 'desktop', '1')
Config.set('kivy', 'log_level', 'debug')

Config.set('kivy', 'pause_on_minimize', '1')

#Config.set('graphics', 'borderless', '0')

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')

#Config.set('graphics', 'width', '1680')
#Config.set('graphics', 'height', '945')

# Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', '1')

#from kivy.core.window import Window


from kivy.app import App
#from kivy.lang import Builder

#from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
#from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

#from kivy.uix.behaviors import FocusBehavior

#from kivy.graphics import Color, Rectangle

#from kivy.properties import ListProperty
#from kivy.properties import StringProperty

import pymongo
from mongo_interface import MongoInterface

#import ui_setting as UISetting
from ui_setting import SettingMainUI
import ui_data_area as UIDataArea

import ui_query as UIQuery


class ManagementWindow(BoxLayout):

    def __init__(self, client_db,  **kargs):

        self.client_db = client_db

        self.db_collections_table = MongoInterface(client_db, "tables")

        self.collections = sorted([i['name']
                                   for i in self.db_collections_table.find_data()])

        self.current_collection = self.collections[0]

        tables_collection = self.db_collections_table.find_data(
            {"name": self.current_collection})

        self.current_collection_categories = tables_collection[0]['category']

        #self.categories_len = 0
        #self.collection_datas_len = 0

        self.rows_per_page = SettingMainUI.data_area_rows_per_page

        #self.category_rows = []
        #self.data_rows = []

        #self.data_row_focused = None

        # call super class init method after initializing all the
        # variable we need

        super(ManagementWindow, self).__init__(**kargs)

        # build widget after calling init method of super class

        self.init_ui()

        self.data_area = UIDataArea.DataArea(self, self.data_container,
                                             self.current_collection_categories,
                                             self.current_collection)

        self.data_container.add_widget(self.data_area)
        # self.update_widget_data(collection=self.current_collection)

    def init_ui(self):

        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.spacing = SettingMainUI.main_spacing
        self.padding = SettingMainUI.main_padding

        self.control_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.05),
            spacing=SettingMainUI.main_spacing)

        self.add_widget(self.control_container)

        self.collection_spinner = Spinner(
            text=self.current_collection,
            font_size=SettingMainUI.main_font_size,
            values=self.collections,
            background_color=(0.8, 0.8, 0.5, 1))

        self.collection_spinner.bind(
            text=lambda spinner, text: self.collection_spinner_changed())

        self.control_container.add_widget(self.collection_spinner)

        self.add_button = Button(
            text='Add',
            font_size=SettingMainUI.main_font_size,
            background_color=(0.3, 0.6, 0.3, 1))

        self.control_container.add_widget(self.add_button)

        self.edit_button = Button(
            text='Edit',
            font_size=SettingMainUI.main_font_size)

        self.control_container.add_widget(self.edit_button)

        self.delete_button = Button(
            text='Delete',
            font_size=SettingMainUI.main_font_size,
            background_color=(0.8, 0.2, 0.2, 1))

        self.control_container.add_widget(self.delete_button)

        # self.categories_container = BoxLayout(
        #    orientation='horizontal',
        #    size_hint=(1, 0.05),
        #    spacing=SettingMainUI.main_spacing)

        # self.add_widget(self.categories_container)

        self.data_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            spacing=SettingMainUI.main_spacing)

        self.add_widget(self.data_container)

        self.page_control_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.05),
            spacing=SettingMainUI.main_spacing)

        self.add_widget(self.page_control_container)

        self.first_page_button = Button(
            text='First Page',
            font_size=SettingMainUI.main_font_size)

        self.page_control_container.add_widget(self.first_page_button)

        self.previous_page_button = Button(text='Previous Page',
                                           font_size=SettingMainUI.main_font_size)

        self.page_control_container.add_widget(self.previous_page_button)

        self.next_page_button = Button(text='Next Page',
                                       font_size=SettingMainUI.main_font_size)

        self.page_control_container.add_widget(self.next_page_button)

        self.last_page_button = Button(text='Last Page',
                                       font_size=SettingMainUI.main_font_size)

        self.page_control_container.add_widget(self.last_page_button)

    # def update_widget_data(self, collection=None):

    #    tables_collection = self.db_table.find_data({"name": collection})

    #    self.collection_categories = tables_collection[0]['category']

    #    new_len = len(self.collection_categories)

    #    c = self.ids['category_row']
    #    d = self.ids['data_area']

    #    for i in self.category_row:
    #        c.remove_widget(i)

    #    for i in self.data_rows:
    #        d.remove_widget(i)

    #    self.categories_len = new_len

    #    for i in range(0, self.categories_len):
    #        try:
    #            label = self.collection_categories[i]

    #        except IndexError:
    #            label = ''

    #        table_label = CustomLabel(id="category_row_{}".format(str(i)),
    #                                  text=str(label),
    #                                  bg_color=[0.1, 0.25, 0.4, 1])

    #        self.ids['category_row'].add_widget(table_label)
    #        self.category_row.append(table_label)

    #    db_collection = MongoInterface(self.client_db, collection)
    #    collection_datas = db_collection.find_data()

    #    self.collection_datas_len = collection_datas.count()

    #    for i in range(0, self.rows_per_page):

    #        try:
    #            datas = collection_datas[i]
    #        except IndexError:
    #            datas = None

    #        data_row = DataAreaRow(self, self.ids['data_area'],
    #                               self.collection_categories,
    #                               datas)

    #        self.data_rows.append(data_row)

    # def update_data(self):

    #    db_collection = MongoInterface(self.client_db,
    #                                   self.current_collection)

    #    collection_datas = db_collection.find_data()

    #    for i in range(0, self.rows_per_page):

    #        try:
    #            datas = collection_datas[i]
    #        except IndexError:
    #            datas = None

    #        self.data_rows[i].set_data(
    #            self.collection_categories,
    #            datas)

    def collection_spinner_changed(self):

        tables_collection = self.db_collections_table.find_data(
            {"name": self.collection_spinner.text})

        self.current_collection_categories = tables_collection[0]['category']

        self.current_collection = self.collection_spinner.text

        self.data_area.categories = self.current_collection_categories
        self.data_area.update_widget()

        # data_area = UIDataArea.DataArea(self, self.data_container,
        #                                self.current_collection_categories,
        #                                self.current_collection)

        print(self.collection_spinner.text)
        print(self.current_collection)
        print(self.current_collection_categories)

        # self.update_widget_data(self.current_collection)

    def show_data_popup(self, title, operation):
        pass
    #    p = DataPopUp(title, self, 'add', self.client_db,
    #                  self.current_collection, self.collection_categories)
    #    p.open()

    def show_delete_popup(self):
        pass
    #    p = DeleteConfirmationPopUp(self,
    #                                self.data_row_focused,
    #                                self.client_db,
    #                                self.current_collection)

    #    p.open()


class ManagementApp(App):

    db_connection = ('localhost', 27017)
    db_collections = 'tifana_db_test'

    def __init__(self, **kargs):

        #self.client = pymongo.MongoClient(
        #    self.db_connection[0],
        #    self.db_connection[1])

        #self.db = self.client[self.db_collections]

        super(ManagementApp, self).__init__(**kargs)

    def build(self):
        #return ManagementWindow(self.db)
        return UIQuery.QueryScreen()

    def end(self):
        pass
        #self.client.close()


if __name__ == '__main__':

    app = ManagementApp()
    app.run()
    app.end()
