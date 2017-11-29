from pymongo import DESCENDING as DESCENDING
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection as MongoCollection
import unittest
from database.database import *
from database.network import *


class MongoDB(Database):

    def __init__(self, ip=server_ip, port=mongo_port):
        client = MongoClient(ip, port)
        super().__init__(client.library.my_collection, MONGODB)

    def create_temp_db(self) -> TempDatabase:
        pass

    def load_from_temp_db(self, database: TempDatabase):
        pass

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
        try:
            res = self.client.find({"_id": id_}).next()
            return Card.create_from_dict({key: res[key] for key in res if key != '_id'})
        except:
            return None

    def clear_db(self):
        return self.client.drop()

    def get_all_documents(self):
        return self.client.find()

    def get_all_keys(self):
        only_ids_cursor = self.client.find( {}, {'_id' : 1 } )
        list = []
        for elem in only_ids_cursor:
            list.append(elem['_id'])
        return list

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


class MongoTest(unittest.TestCase):
    def test_add_and_get(self):
        mongoDB = MongoDB()
        card = Card('Vova007', 'Artur', '2k17', None)
        mongoDB.add_card('1',card)
        self.assertIsInstance(mongoDB.get_card('1'), Card)
        mongoDB.clear_db()

    def test_update(self):
        mongoDB = MongoDB()
        card = Card('Vova007', 'Artur', '2k17', None)
        mongoDB.add_card('1', card)
        old_card = mongoDB.get_card('1')
        old_card_tuple = (old_card.title,old_card.author,old_card.year, old_card.history)
        card_for_update = Card('Spica', 'Spicin', '1980', None)
        mongoDB.update_card('1',card_for_update)
        updated_card = mongoDB.get_card('1')
        new_card_tuple = (updated_card.title,updated_card.author,updated_card.year, updated_card.history)
        self.assertNotEqual(old_card_tuple,new_card_tuple, 'Comparing old and new cards')
        mongoDB.clear_db()

    def test_remove(self):
        mongoDB = MongoDB()
        card = Card('Vova007', 'Artur', '2k17', None)
        mongoDB.add_card('1', card)
        mongoDB.remove_card('1')
        search_result = mongoDB.get_card('1')
        self.assertIsNone(search_result)
        mongoDB.clear_db()

    def test_get_max_id(self):
        mongoDB = MongoDB()
        firstCard = Card('Vova007', 'Artur', '2k17', None)
        secondCard = Card('Vova007', 'Artur', '2k17', None)
        thirdCard = Card('Vova007', 'Artur', '2k17', None)
        mongoDB.add_card('2',firstCard)
        mongoDB.add_card('3', secondCard)
        mongoDB.add_card('4', thirdCard)
        self.assertEqual(mongoDB.get_max_id(),4)
        mongoDB.clear_db()

    def test_clear_db(self):
        mongoDB = MongoDB()
        mongoDB.clear_db()
        self.assertEqual(mongoDB.get_all_documents().count(), 0)

    def test_is_empty(self):
        mongoDB = MongoDB()
        card = Card('Vova007', 'Artur', '2k17', None)
        mongoDB.add_card('1', card)
        self.assertEqual(mongoDB.is_empty(), False)
        mongoDB.clear_db()
        self.assertEqual(mongoDB.is_empty(), True)

    def test_get_all_keys(self):
        mongoDB = MongoDB()
        mongoDB.clear_db()
        card = Card('Vova007', 'Artur', '2k17', None)
        first_id = '1'
        second_id = '2'
        third_id = '3'
        mongoDB.add_card(first_id, card)
        mongoDB.add_card(second_id, card)
        mongoDB.add_card(third_id, card)
        all_keys = mongoDB.get_all_keys()
        self.assertTrue(all((first_id in all_keys, second_id in all_keys, third_id in all_keys)))