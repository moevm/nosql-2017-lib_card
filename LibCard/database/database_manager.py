from database.memcached import Memcached
from database.mongo import MongoDB
from database.neo4j import Neo4j
from database.database import *


class DatabaseManager:

    def __init__(self):
        self._memcached = Memcached()
        self._neo4j = Neo4j()
        self._mongodb = MongoDB()

        self._curr_db: Database = self._memcached

    def switch_to_database(self, database: DBTYPE):

        temp_db: TempDatabase = self._curr_db.create_temp_db()
        old_db: Database = self._curr_db

        if database == MEMCACHED:
            self._curr_db = self._memcached

        elif database == MONGODB:
            self._curr_db = self._mongodb

        elif database == NEO4J:
            self._curr_db = self._neo4j

        else:
            raise AssertionError("undefined database")

        old_db.clear_db()
        self._curr_db.load_from_temp_db(temp_db)

    def create_temp_db(self) -> TempDatabase:
        pass

    def load_from_temp_db(self, database: TempDatabase):
        pass

    def clear_db(self):
        self._curr_db.clear_db()

    def add_card(self, id_, title, author, year):
        self._curr_db.add_card(id_, Card(title, author, year, None))

    def remove_card(self, id_):
        self._curr_db.remove_card(id_)

    def update_card(self, id_, name, author, year):
        self._curr_db.update_card(id_, Card(name, author, year, None))

    def get_card(self, id_) -> Card:
        return self._curr_db.get_card(id_)


def database_manager_tests():
    db: DatabaseManager = DatabaseManager()
    db.add_card("2", "Test title", "Artur", "2k17")
    json = db.get_card("2")
    print('memcached:', json)

    db.switch_to_database(MONGODB)
    db.add_card("2", "Test title", "Artur", "2k17")
    json = db.get_card("2")
    print('mongodb:', json)

    db.switch_to_database(NEO4J)
    db.add_card("2", "Test title", "Artur", "2k17")
    json = db.get_card("2")
    print('neo4j:', json)


if __name__ == '__main__':
    database_manager_tests()
