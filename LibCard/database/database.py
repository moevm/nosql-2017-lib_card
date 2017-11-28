from database.card import Card
from database.temp_database import TempDatabase
from typing import List


DBTYPE = str
MEMCACHED = 'memcached'
MONGODB = 'mongo db'
NEO4J = 'neo4j'


class Database:

    def __init__(self, client, type_):
        self.client = client
        self.type = type_

    def create_temp_db(self) -> TempDatabase:
        pass

    def load_from_temp_db(self, database: TempDatabase):
        pass

    def clear_db(self):
        pass

    def add_card(self, id_: str, card: Card) -> None:
        pass

    def remove_card(self, id_):
        pass

    def update_card(self, id_, card: Card) -> None:
        pass

    def get_card(self, id_) -> Card:
        pass

    def is_empty(self) -> bool:
        pass

    def get_max_id(self) -> int:
        pass

    def get_all_cards(self) -> List[Card]:
        pass
