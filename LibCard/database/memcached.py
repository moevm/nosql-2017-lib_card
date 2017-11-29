import unittest
from database.network import server_ip, memcached_port
from database.database import *
from database.card import Card
from memcache import Client as MemcacheClient


class Memcached(Database):

    def __init__(self, ip=server_ip, port=memcached_port):
        super().__init__(MemcacheClient([f'{ip}:{port}'], debug=0), MEMCACHED)
        self.client: MemcacheClient
        self.keys = self.client.get('keys')
        if self.keys is None:
            self.keys = []

    def add_card(self, id_: str, card: Card):
        self.client: MemcacheClient
        self.client.delete(id_)
        self.client.add(id_, {'title': card.title,
                              'author': card.author,
                              'year': card.year,
                              'image': card.image,
                              'history': card.history})
        if id_ not in self.keys:
            self.keys += [id_]
            self.client.set('keys', self.keys)

    def get_card(self, id_):
        if id_ in self.keys:
            return Card.create_from_dict(self.client.get(id_))
        else:
            return None

    def remove_card(self, id_):
        if id_ in self.keys:
            self.client.delete(id_)
            del self.keys[self.keys.index(id_)]
            self.client.set('keys', self.keys)

    def update_card(self, id_, card: Card) -> None:
        old = self.get_card(id_)
        card.image = old.image
        card.history = old.history
        self.add_card(id_, card)

    def get_max_id(self):
        return max(int(i) for i in self.keys) if self.keys else -1

    def is_empty(self):
        return False if len(self.keys) > 0 else True

    def clear_db(self):
        self.client: MemcacheClient
        for key in self.keys:
            self.client.delete(key)
        self.keys = []
        self.client.set('keys', self.keys)

    def get_all_keys(self):
        return self.keys


class MemcachedTest(unittest.TestCase):
    def test_add_and_get(self):
        memcached = Memcached()
        card = Card('Vova007', 'Artur', '2k17', None, None)
        memcached.add_card('1', card)
        self.assertIsInstance(memcached.get_card('1'), Card)
        memcached.clear_db()

    def test_update(self):
        memcached = Memcached()
        card = Card('Vova007', 'Artur', '2k17', None, None)
        memcached.add_card('1', card)
        old_card = memcached.get_card('1')
        old_card_tuple = (old_card.title, old_card.author, old_card.year, old_card.history)
        card_for_update = Card('Spica', 'Spicin', '1980', None, None)
        memcached.update_card('1', card_for_update)
        updated_card = memcached.get_card('1')
        new_card_tuple = (updated_card.title, updated_card.author, updated_card.year, updated_card.history)
        self.assertNotEqual(old_card_tuple, new_card_tuple, 'Comparing old and new cards')
        memcached.clear_db()

    def test_remove(self):
        memcached = Memcached()
        card = Card('Vova007', 'Artur', '2k17', None, None)
        memcached.add_card('1', card)
        memcached.remove_card('1')
        search_result = memcached.get_card('1')
        self.assertIsNone(search_result)
        memcached.clear_db()

    def test_get_max_id(self):
        memcached = Memcached()
        firstCard = Card('Vova007', 'Artur', '2k17', None, None)
        secondCard = Card('Vova007', 'Artur', '2k17', None, None)
        thirdCard = Card('Vova007', 'Artur', '2k17', None, None)
        memcached.add_card('2', firstCard)
        memcached.add_card('3', secondCard)
        memcached.add_card('4', thirdCard)
        self.assertEqual(memcached.get_max_id(), 4)
        memcached.clear_db()

    def test_clear_db(self):
        memcached = Memcached()
        memcached.clear_db()
        self.assertEqual(memcached.is_empty(), True)

    def test_is_empty(self):
        memcached = Memcached()
        card = Card('Vova007', 'Artur', '2k17', None, None)
        memcached.add_card('1', card)
        self.assertEqual(memcached.is_empty(), False)
        memcached.clear_db()
        self.assertEqual(memcached.is_empty(), True)

    def test_get_all_cards(self):
        memcached = Memcached()
        firstCard = Card('Vova007', 'Artur', '2k17', None, None)
        secondCard = Card('Vova007', 'Artur', '2k17', None, None)
        thirdCard = Card('Vova007', 'Artur', '2k17', None, None)
        memcached.add_card('2', firstCard)
        memcached.add_card('3', secondCard)
        memcached.add_card('4', thirdCard)
        self.assertEqual(memcached.get_all_keys(), ['2', '3', '4'])
        memcached.clear_db()
