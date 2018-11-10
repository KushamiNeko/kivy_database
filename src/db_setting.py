from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class DBCategoriesSetting:

    # full categories store information that actually need to be stored into database
    # appears to the new item screen and edit item screen
    full_categories = ['product_id', 'product_name', 'category',
                       'condition', 'cost', 'price', 'store', 'description']

    # query_categories store information that appears to the query screen
    query_categories = [0, 1, 2, 3, 5, 6]


class DBCategoriesLanguage:

    full_categories = {DBCategoriesSetting.full_categories[0]: 'Product ID',
                       DBCategoriesSetting.full_categories[1]: 'Product Name',
                       DBCategoriesSetting.full_categories[2]: 'Category',
                       DBCategoriesSetting.full_categories[3]: 'Condition',
                       DBCategoriesSetting.full_categories[4]: 'Cost',
                       DBCategoriesSetting.full_categories[5]: 'Price',
                       DBCategoriesSetting.full_categories[6]: 'Store',
                       DBCategoriesSetting.full_categories[7]: 'Description'}
