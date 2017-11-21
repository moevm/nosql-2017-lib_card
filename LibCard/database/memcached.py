from database.network import server_ip, memcached_port
from database.database import *
from database.card import Card
from memcache import Client as MemcacheClient


class Memcached(Database):

    def __init__(self, ip=server_ip, port=memcached_port):
        super().__init__(MemcacheClient([f'{ip}:{port}'], debug=0), MEMCACHED)
        self.client: MemcacheClient

    def add_card(self, id_: str, card: Card):
        self.client.set(id_, {'title': card.title, 'author': card.author, 'year': card.year, 'history': None})

    def get_card(self, id_):
        return Card.create_from_dict(self.client.get(id_))
