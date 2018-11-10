import kivy
from kivy.uix.boxlayout import BoxLayout

#from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.uix.screenmanager import ScreenManager, Screen

from ui_setting import SettingMainUI
from ui_custom_label import CustomLabel

from db_setting import DBCategoriesSetting
from db_setting import DBCategoriesLanguage


class QueryScreenLanguage:
    screen_label = u'查詢'


class QueryField(BoxLayout):

    def __init__(self, label, db_category, **kargs):

        self.db_category = db_category

        super(QueryField, self).__init__(**kargs)

        self.orientation = 'horizontal'
        self.size_hint = (1, 1)
        self.spacing = SettingMainUI.main_spacing
        self.padding = SettingMainUI.main_padding

        self.label = CustomLabel(
            text=label,
            bg_color=SettingMainUI.default_color_blue)

        self.add_widget(self.label)

        self.input = TextInput(
            background_color=SettingMainUI.default_color_grey,
            foreground_color=(0.8, 0.8, 0.8, 1),
            font_name='RobotoMono-Regular',
            text=QueryScreenLanguage.screen_label)

        self.add_widget(self.input)


class QueryScreen(Screen):

    def __init__(self, **kargs):

        self.query_fields = []

        super(QueryScreen, self).__init__(**kargs)

        self.main_container = BoxLayout(
            orientation='vertical',
            padding=SettingMainUI.main_padding,
            spacing=SettingMainUI.main_spacing)

        self.add_widget(self.main_container)

        self.screen_label = CustomLabel(
            text=QueryScreenLanguage.screen_label,
            bg_color=(0.2, 0.4, 0.3, 1),
            size_hint=(1, 1),
            font_name='RobotoMono-Regular')

        self.main_container.add_widget(self.screen_label)

        #######################################################################

        self.db_build_query_field()

        #######################################################################

        self.control_container = BoxLayout(
            orientation='horizontal',
            padding=SettingMainUI.main_padding,
            spacing=SettingMainUI.main_spacing)

        self.main_container.add_widget(self.control_container)

        self.query_button = Button(
            text='Query')

        self.query_button.bind(on_press=lambda x: self.get_query_info())

        self.control_container.add_widget(self.query_button)

        self.clear_button = Button(
            text='Clear')

        self.clear_button.bind(on_press=lambda x: self.clear_query_input())

        self.control_container.add_widget(self.clear_button)

    def db_build_query_field(self):
        for i in DBCategoriesSetting.query_categories:
            key = DBCategoriesSetting.full_categories[i]
            language_label = DBCategoriesLanguage.full_categories[key]

            field = QueryField(language_label, key)

            self.main_container.add_widget(field)

            self.query_fields.append(field)

    def get_query_info(self):
        re = {}

        for i in self.query_fields:
            re[i.db_category] = i.input.text

        print(re)
        return re

    def clear_query_input(self):
        for i in self.query_fields:
            i.input.text = ''

        print('clear input')
