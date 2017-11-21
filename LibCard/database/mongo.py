from network import server_ip, mongo_port
from database import *
from card import Card
import pymongo
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
            return int(self.get_all_documents().sort([('_id', pymongo.DESCENDING)])[0]['_id'])
        except:
            return -1

    def is_empty(self) -> bool:
        return False if self.get_all_documents().count() > 0 else True


mongoDB = MongoDB()

#firstCard = Card('Vovan007', 'Artur Azarau', '2017', None)
secondCard = Card('Vovan007', 'Artur Azar', '2017', None)
thirdCard = Card('Vovan007', 'Artur Aza', '2017', None)
#mongoDB.add_card('1',firstCard)
# mongoDB.add_card('2',secondCard)
# mongoDB.add_card('3',thirdCard)
# card = Card('Vovan008', 'Artur Azarov', '201734234', None)
# mongoDB.update_card('1', card)
#getCard = monogDB.get_card(1)
#print(getCard.title)
mongoDB.clear_db()
#monogDB.remove_card('1')
# all_documents = mongoDB.get_all_documents()
# for element in all_documents:
#     print(element)

a = mongoDB.get_max_id()
print(a)
b = mongoDB.is_empty()
print(b)
# for doc in :
#     print(doc['_id'])