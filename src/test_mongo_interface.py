import unittest

import pymongo
import mongo_interface as MongoInterface

from random import randint


class TestCustomerDB(unittest.TestCase):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['tifana_db_test']
    db_customer = MongoInterface.MongoInterface(db, "customers")

    testTime = 100

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add(self):

        newCustomer = {
            "name": "Bill Gates",
            "phone": "0000000000",
            "email": "microsoft@microsoft.com",
            "line": "microsoft",
            "facebook": "microsoft"}

        for i in range(0, self.testTime):

            combination = randint(1, 5)

            query = {}
            for i in range(0, combination):

                while True:
                    item = randint(0, 4)
                    if query.get(list(newCustomer.items())[item][0]) is None:
                        query[list(newCustomer.items())[item][0]] = list(
                            newCustomer.items())[item][1]
                        break

            self.db_customer.delete_data(query)

            query = {}
            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 2)

            self.db_customer.add_data(newCustomer)

            query = {}
            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 3)

            query = {}
            for i in range(0, combination):

                while True:
                    item = randint(0, 4)
                    if query.get(list(newCustomer.items())[item][0]) is None:
                        query[list(newCustomer.items())[item][0]] = list(
                            newCustomer.items())[item][1]
                        break

            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 1)

            customer = customers[0]

            self.assertEqual(customer['name'], newCustomer['name'])
            self.assertEqual(customer['name'], "Bill Gates")
            self.assertEqual(customer['phone'], newCustomer['phone'])
            self.assertEqual(customer['phone'], "0000000000")
            self.assertEqual(customer['line'], newCustomer['line'])
            self.assertEqual(customer['line'], "microsoft")
            self.assertEqual(customer['facebook'], newCustomer['facebook'])
            self.assertEqual(customer['facebook'], "microsoft")
            self.assertEqual(customer['email'], newCustomer['email'])
            self.assertEqual(customer['email'], "microsoft@microsoft.com")

            query = {}
            for i in range(0, combination):

                while True:
                    item = randint(0, 4)
                    if query.get(list(newCustomer.items())[item][0]) is None:
                        query[list(newCustomer.items())[item][0]] = list(
                            newCustomer.items())[item][1]
                        break

            self.db_customer.delete_data(query)

            query = {}
            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 2)


        query = {}
        customers = self.db_customer.find_data(query)

        self.assertEqual(customers.count(), 2)

    def test_delete(self):

        self.db_customer.delete_data({"name": "Peter Drucker"})
        self.db_customer.delete_data({"name": "Warrent Buffett"})

        query = {}
        customers = self.db_customer.find_data(query)

        self.assertEqual(customers.count(), 2)

        newCustomer = {
            "name": "Warrent Buffett",
            "phone": "9999999999",
            "email": "Berkshire Hathaway@Berkshire Hathaway.com",
            "line": "Berkshire Hathaway",
            "facebook": "Berkshire Hathaway"}

        for i in range(0, self.testTime):

            combination = randint(1, 5)

            query = {}
            for i in range(0, combination):

                while True:
                    item = randint(0, 4)
                    if query.get(list(newCustomer.items())[item][0]) is None:
                        query[list(newCustomer.items())[item][0]] = list(
                            newCustomer.items())[item][1]
                        break

            self.db_customer.add_data(newCustomer)

            query = {}
            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 3)

            query = {}
            for i in range(0, combination):

                while True:
                    item = randint(0, 4)
                    if query.get(list(newCustomer.items())[item][0]) is None:
                        query[list(newCustomer.items())[item][0]] = list(
                            newCustomer.items())[item][1]
                        break

            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 1)

            customer = customers[0]

            self.assertEqual(customer['name'], newCustomer['name'])
            self.assertEqual(customer['name'], "Warrent Buffett")
            self.assertEqual(customer['phone'], newCustomer['phone'])
            self.assertEqual(customer['phone'], "9999999999")
            self.assertEqual(customer['line'], newCustomer['line'])
            self.assertEqual(customer['line'], "Berkshire Hathaway")
            self.assertEqual(customer['facebook'], newCustomer['facebook'])
            self.assertEqual(customer['facebook'], "Berkshire Hathaway")
            self.assertEqual(customer['email'], newCustomer['email'])
            self.assertEqual(
                customer['email'], "Berkshire Hathaway@Berkshire Hathaway.com")

            query = {}
            for i in range(0, combination):

                while True:
                    item = randint(0, 4)
                    if query.get(list(newCustomer.items())[item][0]) is None:
                        query[list(newCustomer.items())[item][0]] = list(
                            newCustomer.items())[item][1]
                        break

            self.db_customer.delete_data(query)

            query = {}
            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 2)

        query = {}
        customers = self.db_customer.find_data(query)

        self.assertEqual(customers.count(), 2)

    def test_query(self):

        data = {
            "name": "Onion Huang",
            "phone": "0925310801",
            "line": "missing10630",
            "email": "missing10630@gmail.com",
            "facebook": "missing10630"}

        for i in range(0, self.testTime):
            combination = randint(1, 5)

            query = {}
            for i in range(0, combination):

                while True:
                    item = randint(0, 4)
                    if query.get(list(data.items())[item][0]) is None:
                        query[list(data.items())[item][0]] = list(
                            data.items())[item][1]
                        break

            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 1)

            customer = customers[0]

            self.assertEqual(customer['name'], "Onion Huang")
            self.assertEqual(customer['phone'], "0925310801")
            self.assertEqual(customer['line'], "missing10630")
            self.assertEqual(customer['facebook'], "missing10630")
            self.assertEqual(customer['email'], "missing10630@gmail.com")

        data = {'name': "Magical Otaka",
                'phone': "0936242172",
                'line': None,
                'facebook': None,
                'email': None}

        for i in range(0, self.testTime):
            combination = randint(1, 5)

            query = {}
            for i in range(0, combination):

                while True:
                    item = randint(0, 4)
                    if query.get(list(data.items())[item][0]) is None:
                        query[list(data.items())[item][0]] = list(
                            data.items())[item][1]
                        break

            customers = self.db_customer.find_data(query)

            self.assertEqual(customers.count(), 1)

            customer = customers[0]

            self.assertEqual(customer['name'], "Magical Otaka")
            self.assertEqual(customer['phone'], "0936242172")
            self.assertEqual(customer['line'], None)
            self.assertEqual(customer['facebook'], None)
            self.assertEqual(customer['email'], None)

        query = {"name": "Peter Drucker"}
        customers = self.db_customer.find_data(query)

        self.assertEqual(customers.count(), 0)


if __name__ == '__main__':
    unittest.main()
