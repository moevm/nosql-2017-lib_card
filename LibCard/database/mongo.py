from database.network import server_ip, mongo_port
from database.database import *
from database.card import Card
from pymongo import DESCENDING as DESCENDING
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection as MongoCollection


class MongoDB(Database):

    def __init__(self, ip=server_ip, port=mongo_port):
        client = MongoClient(ip, port)
        super().__init__(client.library.my_collection, MONGODB)

    def add_card(self, id_: str, card: Card):
        self.client: MongoCollection
        try:
            self.client.insert_one({"_id": id_,
                                    "title": card.title,
                                    "author": card.author,
                                    "year": card.year,
                                    "history": None})
        except:
            self.client.replace_one(self.client.find({"_id": id_}).next(),
                                    {"_id": id_,
                                     "title": card.title,
                                     "author": card.author,
                                     "year": card.year,
                                     "history": None})

    def get_card(self, id_):
        self.client: MongoDatabase
        res = self.client.find({"_id": id_}).next()
        return Card.create_from_dict({key: res[key] for key in res if key != '_id'})

    def clear_db(self):
        return self.client.drop()

    def get_all_documents(self):
        return self.client.find()

    def remove_card(self, _id):
        self.client.delete_one({ '_id' : _id })

    def update_card(self, _id, card: Card):
        try:
            self.client.replace_one(self.client.find({"_id": _id}).next(),
                                {"_id": _id,
                                 "title": card.title,
                                 "author": card.author,
                                 "year": card.year,
                                 "history": None})
        except:
            print('No such card to update')

    def get_max_id(self) -> int:
        try:
            return int(self.get_all_documents().sort([('_id', DESCENDING)])[0]['_id'])
        except:
            return -1

    def is_empty(self) -> bool:
        return False if self.get_all_documents().count() > 0 else True
