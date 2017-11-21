from database.memcached import Memcached
from database.mongo import MongoDB
from database.neo4j import Neo4j
from database.database import *


class DatabaseManager:

    def __init__(self):
        self._memcached = Memcached()
        self._neo4j = Neo4j()
        self._mongodb = MongoDB()
        self._curr_db: Database

        is_neo4j_empty = self._neo4j.is_empty()
        is_mongo_empty = self._mongodb.is_empty()

        if is_neo4j_empty and is_mongo_empty:
            self._curr_db = self._memcached

        elif is_neo4j_empty and not is_mongo_empty:
            self._curr_db = self._mongodb

        elif not is_neo4j_empty and is_mongo_empty:
            self._curr_db = self._neo4j

        else:
            self._mongodb.clear_db()
            self._curr_db = self._neo4j

        self._id = self._generate_ids()

    def _generate_ids(self):
        id_: int = self._curr_db.get_max_id()
        while True:
            id_ += 1
            yield str(id_)

    def _next_id(self):
        return next(self._id)

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

    def add_card(self, title, author, year):
        self._curr_db.add_card(self._next_id(), Card(title, author, year, None))

    def remove_card(self, id_):
        self._curr_db.remove_card(id_)

    def update_card(self, name, author, year):
        self._curr_db.update_card(self._next_id(), Card(name, author, year, None))

    def get_card(self, id_) -> Card:
        return self._curr_db.get_card(id_)

    def print_curr_database(self) -> str:
        if self._curr_db == self._memcached:
            return MEMCACHED
        elif self._curr_db == self._mongodb:
            return MONGODB
        elif self._curr_db == self._neo4j:
            return NEO4J


def database_manager_tests():
    db: DatabaseManager = DatabaseManager()
    db.switch_to_database(MEMCACHED)
    db.add_card("Test title", "Artur", "2k17")
    json = db.get_card("2")
    print('memcached:', json)
    '''
    db.switch_to_database(MONGODB)
    db.add_card("Test title", "Artur", "2k17")
    json = db.get_card("2")
    print('mongodb:', json)
    '''
    db.switch_to_database(NEO4J)
    db.add_card("Test title", "Artur", "2k17")
    json = db.get_card("2")
    print('neo4j:', json)


if __name__ == '__main__':
    database_manager_tests()
