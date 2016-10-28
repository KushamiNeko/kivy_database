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

db_connection = ('localhost', 27017)
db_collections = 'tifana_db_test'


class CustomLabel(Label):
    bg_color = ListProperty([0.15, 0.15, 0.15, 1])

    def __init__(self, bg_color=None, **kargs):
        super(CustomLabel, self).__init__(**kargs)

        if bg_color:
            self.bg_color = bg_color


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
        super(DataPopUpRow, self).__init__(**kargs)

        self.field_name = field_name

        if field_data:
            self.field_data = field_data

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


class ManagementWindow(BoxLayout):

    client = pymongo.MongoClient(db_connection[0], db_connection[1])
    db = client[db_collections]

    db_table = MongoInterface(db, "tables")

    tables = sorted([i['name'] for i in db_table.find_data()])

    rows_per_page = 15

    def __init__(self, **kargs):
        super(ManagementWindow, self).__init__(**kargs)

        self.categories_len = 0

        self.current_collection = self.tables[0]

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
                                      text=str(label), bg_color=[0.1, 0.25, 0.4, 1])
            self.ids['category_row'].add_widget(table_label)

        db_customer = MongoInterface(self.db, collection)
        customers = db_customer.find_data()

        for i in range(0, self.rows_per_page):
            layout = BoxLayout(id="data_row_{}".format(str(i)),
                               orientation='horizontal',
                               size_hint_x=1,
                               size_hint_y=1,
                               spacing=2)

            for j in range(0, self.categories_len):
                try:
                    customer = customers[i]
                    label = CustomLabel(id="{}_{}".format(
                        str(i), self.collection_categories[j]),
                        text=str(customer[self.collection_categories[j]]))

                except (IndexError, KeyError):
                    label = CustomLabel(text='')

                layout.add_widget(label)

            self.ids['data_area'].add_widget(layout)

    def update_data(self, row=None, field=None):
        pass

    def show_data_popup(self, title, operation):
        p = DataPopUp(title, self, 'add', self.db, self.current_collection,
                      self.collection_categories)
        p.open()

    def show_confirmation_popup(self):
        p = ConfirmationPopUp()
        p.open()


class ManagementApp(App):

    def build(self):
        self.program = ManagementWindow()
        return self.program

    def end(self):
        self.program.close_db()


if __name__ == '__main__':

    app = ManagementApp()
    app.run()
    app.end()
