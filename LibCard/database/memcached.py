from database.network import server_ip, memcached_port
from database.database import *
from database.card import Card
from memcache import Client as MemcacheClient


class Memcached(Database):

    def __init__(self, ip=server_ip, port=memcached_port):
        super().__init__(MemcacheClient([f'{ip}:{port}'], debug=0), MEMCACHED)
        self.client: MemcacheClient
        self.keys = []

    def create_temp_db(self) -> TempDatabase:
        pass

    def load_from_temp_db(self, database: TempDatabase):
        pass

    def add_card(self, id_: str, card: Card):

        self.client.set(id_, {'title': card.title, 'author': card.author, 'year': card.year, 'history': None})
        self.keys += [id_]

    def get_card(self, id_):
        if id_ in self.keys:
            return Card.create_from_dict(self.client.get(id_))
        else:
            return None

    def get_max_id(self):
        return max(int(i) for i in self.keys) if self.keys else -1

    def is_empty(self):
        return len(self.keys) > 0

    def clear_db(self):
        self.client: MemcacheClient
        for key in self.keys:
            self.client.delete(key)
        self.keys = []


def memcached_tests():
    db = Memcached()


if __name__ == '__main__':
    memcached_tests()
