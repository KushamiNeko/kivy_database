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

from kivy.core.window import Window


from kivy.app import App
from kivy.lang import Builder

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.properties import ListProperty
from kivy.properties import StringProperty

import pymongo
from mongo_interface import MongoInterface


class CustomLabel(Label):
    bg_color = ListProperty([0.15, 0.15, 0.15, 1])

    def __init__(self, bg_color=None, **kargs):

        if bg_color:
            self.bg_color = bg_color

        super(CustomLabel, self).__init__(**kargs)


class DataPopUp(Popup):

    def __init__(self,
                 title,
                 parent_window,
                 operation_type,
                 db,
                 collection,
                 categories,
                 **kargs):

        super(DataPopUp, self).__init__(**kargs)

        self.title = title

        self.db = db
        self.db_collection = collection
        self.categories = categories

        self.parent_window = parent_window

        self.db_data = {}

        for i in range(0, len(categories)):
            try:
                label = categories[i]

            except IndexError:
                label = ''

            data_row = DataPopUpRow(field_name=label, field_data=None)
            self.ids['data_popup_rows'].add_widget(data_row)

            self.db_data[label] = data_row

        button_layout = BoxLayout(orientation='horizontal', spacing=2)

        add = Button(text='OK', background_color=(0.3, 0.6, 0.3, 1))

        if operation_type == 'add':
            add.on_press = lambda: self.add_data()
        elif operation_type == 'edit':
            add.on_press = lambda: self.edit_data()
        else:
            raise ValueError

        cancel = Button(text='Cancel', background_color=(0.8, 0.2, 0.2, 1),
                        on_press=lambda x: self.dismiss())

        button_layout.add_widget(add)
        button_layout.add_widget(cancel)

        self.ids['data_popup_rows'].add_widget(button_layout)

    def add_data(self):
        db_interface = MongoInterface(self.db, self.db_collection)

        data = {}

        for i in self.db_data.keys():
            value = self.db_data[i].get_data()
            data[i] = value if value else None

        db_interface.add_data(data)
        self.dismiss()

    def edit_data(self):
        self.dismiss()


class DataPopUpRow(BoxLayout):
    field_name = StringProperty('')
    field_data = StringProperty('')

    def __init__(self, field_name, field_data, **kargs):

        self.field_name = field_name

        if field_data:
            self.field_data = field_data

        super(DataPopUpRow, self).__init__(**kargs)

    def get_data(self):
        return self.ids['data_input'].text


class ConfirmationPopUp(Popup):

    answer = False

    def __init__(self, **kargs):
        super(ConfirmationPopUp, self).__init__(**kargs)

    def dismiss(self, answer=False):
        self.answer = answer

        if self.answer:
            print("do something")

        super(ConfirmationPopUp, self).dismiss()


class CategoryAreaRow(BoxLayout):
    pass


class DataAreaRow(BoxLayout):

    # layout = BoxLayout(id="data_row_{}".format(str(i)),
    #                    orientation='horizontal',
    #                    size_hint_x=1,
    #                    size_hint_y=1,
    #                    spacing=2)

    def __init__(self, parent, categories, datas, **kargs):
        super(DataAreaRow, self).__init__(**kargs)

        self.orientation = 'horizontal'
        self.size_hint = (1, 1)
        self.spacing = 2

        self.data_labels = []

        for j in range(0, len(categories)):

            if datas:
                try:
                    data = datas[categories[j]]

                    if data:
                        text = data
                    else:
                        text = ''

                except (IndexError, KeyError):
                    text = ''

                label = CustomLabel(text=text)

            else:
                label = CustomLabel(text='')

            self.add_widget(label)
            self.data_labels.append(label)

        parent.add_widget(self)

    def set_data(self, categories, datas):

        for j in range(0, len(categories)):

            text = ''

            if datas:
                try:
                    data = datas[categories[j]]

                    if data:
                        text = data

                except (IndexError, KeyError):
                    pass

            self.data_labels[j].text = text


class ManagementWindow(BoxLayout):

    #client = pymongo.MongoClient(db_connection[0], db_connection[1])
    #db = client[db_collections]

    #db_table = MongoInterface(db, "tables")

    #tables = sorted([i['name'] for i in db_table.find_data()])
    tables = ListProperty()

    #rows_per_page = 15

    def __init__(self, client_db,  **kargs):

        self.client_db = client_db

        self.db_table = MongoInterface(client_db, "tables")

        self.tables = sorted([i['name'] for i in self.db_table.find_data()])

        self.current_collection = self.tables[0]

        self.categories_len = 0
        self.collection_datas_len = 0

        self.rows_per_page = 15

        self.data_rows = []

        # call super class init method after initializing all the
        # variable we need

        super(ManagementWindow, self).__init__(**kargs)

        # build widget after calling init method of super class

        self.update_widget_data(collection=self.current_collection)

    def close_db(self):
        self.client.close()

    def clean_widget(self, old_len, new_len):
        pass

    def update_widget_data(self, collection=None):

        tables_collection = self.db_table.find_data({"name": collection})

        self.collection_categories = tables_collection[0]['category']

        new_len = len(self.collection_categories)

        if self.categories_len != new_len:
            self.clean_widget(self.categories_len, new_len)

        self.categories_len = new_len

        for i in range(0, self.categories_len):
            try:
                label = self.collection_categories[i]

            except IndexError:
                label = ''

            table_label = CustomLabel(id="category_row_{}".format(str(i)),
                                      text=str(label),
                                      bg_color=[0.1, 0.25, 0.4, 1])

            self.ids['category_row'].add_widget(table_label)

        db_collection = MongoInterface(self.client_db, collection)
        collection_datas = db_collection.find_data()

        self.collection_datas_len = collection_datas.count()

        for i in range(0, self.rows_per_page):

            try:
                datas = collection_datas[i]
            except IndexError:
                datas = None

            data_row = DataAreaRow(self.ids['data_area'],
                                   self.collection_categories,
                                   datas)

            self.data_rows.append(data_row)

            # layout = BoxLayout(id="data_row_{}".format(str(i)),
            #                   orientation='horizontal',
            #                   size_hint_x=1,
            #                   size_hint_y=1,
            #                   spacing=2)

            # for j in range(0, self.categories_len):
            #    try:
            #        customer = customers[i]
            #        label = CustomLabel(id="{}_{}".format(
            #            str(i), self.collection_categories[j]),
            #            text=str(customer[self.collection_categories[j]]))

            #    except (IndexError, KeyError):
            #        label = CustomLabel(text='')

            #    layout.add_widget(label)

            # self.ids['data_area'].add_widget(layout)

    def update_data(self, row=None, field=None):
        pass

    def show_data_popup(self, title, operation):
        p = DataPopUp(title, self, 'add', self.client_db,
                      self.current_collection, self.collection_categories)
        p.open()

    def show_confirmation_popup(self):
        p = ConfirmationPopUp()
        p.open()


class ManagementApp(App):

    db_connection = ('localhost', 27017)
    db_collections = 'tifana_db_test'

    def __init__(self, **kargs):

        self.client = pymongo.MongoClient(
            self.db_connection[0],
            self.db_connection[1])

        self.db = self.client[self.db_collections]

        super(ManagementApp, self).__init__(**kargs)

    def build(self):
        return ManagementWindow(self.db)

    def end(self):
        self.client.close()


if __name__ == '__main__':

    app = ManagementApp()
    app.run()
    app.end()
