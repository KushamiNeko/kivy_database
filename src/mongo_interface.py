import pymongo


class MongoInterface:

    def __init__(self, db, collection):
        self.db = db

        self.collection = db[collection]

    def add_data(self, data):
        if len(data.items()) >= 1:
            self.collection.insert_one(data)

    def delete_data(self, query):

        if len(query.items()) >= 1:
            self.collection.delete_many(query)

    def find_data(self, query=None):

        if query and len(query.items()) >= 0:
            data = self.collection.find(query)
        else:
            data = self.collection.find()

        return data

    def update_data(self, query, data, operation):
        if len(data.items()) >= 1:

            update = {operation : data}

            if query and len(query.items()) >= 0:
                data = self.collection.update_many(query, update)
            else:
                data = self.collection.update_many({}, update)


