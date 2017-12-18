import unittest
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

        else:
            self._memcached.clear_db()

            if is_neo4j_empty and not is_mongo_empty:
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

    def clear_db(self):
        self._curr_db.clear_db()

    def add_card(self, title, author, year, image) -> str:
        id_ = self._next_id()
        self._curr_db.add_card(id_, Card(title, author, year, None, image))
        return id_

    def remove_card(self, id_):
        self._curr_db.remove_card(id_)

    def update_card(self, id_, title, author, year):
        self._curr_db.update_card(id_, Card(title, author, year, None, None))

    def get_card(self, id_) -> Card:
        return self._curr_db.get_card(id_)

    def get_all_keys(self):
        return self._curr_db.get_all_keys()

    def give_book(self, id_: str, reader: str, date_from: str):
        self._curr_db.give_book(id_, reader, date_from)

    def return_book(self, id_: str, date_to: str):
        self._curr_db.return_book(id_, date_to)

    def print_curr_database(self) -> str:
        if self._curr_db == self._memcached:
            return MEMCACHED
        elif self._curr_db == self._mongodb:
            return MONGODB
        elif self._curr_db == self._neo4j:
            return NEO4J

    def set_test_enviroment(self):
        self.switch_to_database(MONGODB)
        self.clear_db()
        self.add_card('Евгений Онегин', 'А. С. Пушкин', '1831', 'http://biseromania.ru/fgusefusgp/2326')
        self.add_card('С++ для чайников', 'Стефан Р. Дэвис', '2011', 'https://img.yumpu.com/55907147/1/358x526/-.jpg?quality=80')
        self.add_card('Война и мир', 'Лев Толстой', '1869', 'http://merpesnya.ru/uploads/images/v/o/j/vojna_i_mir.jpg')
        self.add_card('Преступление и наказание', 'Ф. М. Достоевский', '1866', 'https://sweetbook.net/uploads/topics/preview/00/00/03/50/f3c22d7a59.jpg')
        self.add_card('Мастер и Маргарита', 'Михаил Булгаков', '1966', 'http://minemshop.ru/images/1012150539.jpg')
        self.add_card('Мертвые души', 'Николай Гоголь', '1842', 'https://cdn.27.ua/799/63/bf/222143_1.jpeg')
        self.add_card('Горе от ума', 'А. Грибоедов', '1862', 'http://minemshop.ru/images/1010251788.jpg')
        self.add_card('Анна Каренина', 'Лев Толстой', '1877', 'https://cdn.27.ua/799/62/98/221848_1.jpeg')
        self.add_card('Руслан и Людмила', 'А. С. Пушкин', '1825', 'http://newbookshop.ru/pictures/1005502028.jpg')

class DatabaseManagerTests(unittest.TestCase):
    def test_switching(self):
        db = DatabaseManager()
        db.switch_to_database(MEMCACHED)
        self.assertEqual(db.print_curr_database(), MEMCACHED)
        db.switch_to_database(MONGODB)
        self.assertEqual(db.print_curr_database(), MONGODB)
        db.switch_to_database(NEO4J)
        self.assertEqual(db.print_curr_database(), NEO4J)

    def test_adding(self):
        db = DatabaseManager()
        db.switch_to_database(MEMCACHED)
        test_card = ("Test title", "Artur", "2k17", 'example.png')
        key = db.add_card(*test_card)
        json = db.get_card(key)
        self.assertEqual((json.title, json.author, json.year, json.image), test_card)
        db.clear_db()

        db.switch_to_database(MONGODB)
        key = db.add_card(*test_card)
        json = db.get_card(key)
        self.assertEqual((json.title, json.author, json.year, json.image), test_card)
        db.clear_db()

        db.switch_to_database(NEO4J)
        key = db.add_card(*test_card)
        json = db.get_card(key)
        self.assertEqual((json.title, json.author, json.year, json.image), test_card)
        db.clear_db()

    def test_choose_right_db_to_start(self):
        db = DatabaseManager()
        db.switch_to_database(MONGODB)
        test_card = ("Test title", "Artur", "2k17", 'example.png')
        db.add_card(*test_card)
        del db

        db = DatabaseManager()
        self.assertEqual(db.print_curr_database(), MONGODB)
        db.clear_db()
        db.switch_to_database(NEO4J)
        db.add_card(*test_card)
        del db

        db = DatabaseManager()
        self.assertEqual(db.print_curr_database(), NEO4J)
        db.clear_db()
        db.switch_to_database(MEMCACHED)
        db.add_card(*test_card)
        del db

        db = DatabaseManager()
        self.assertEqual(db.print_curr_database(), MEMCACHED)

    def test_correct_data_after_reloading_db(self):
        db = DatabaseManager()
        db.switch_to_database(MEMCACHED)
        test_card = ("Test title", "Artur", "2k17", 'example.png')
        key = db.add_card(*test_card)
        del db

        db = DatabaseManager()
        result = db.get_card(key)
        self.assertEqual((result.title, result.author, result.year, result.image), test_card)
        db.clear_db()

        test_card = ("Another Test title", "Vladimir", "1996", 'example.png')
        db.switch_to_database(NEO4J)
        key = db.add_card(*test_card)
        del db

        db = DatabaseManager()
        result = db.get_card(key)
        self.assertEqual((result.title, result.author, result.year, result.image), test_card)
        db.clear_db()

        test_card = ("Other Test title", "Igorek", "2017", 'example.png')
        db.switch_to_database(MONGODB)
        key = db.add_card(*test_card)
        del db

        db = DatabaseManager()
        result = db.get_card(key)
        self.assertEqual((result.title, result.author, result.year, result.image), test_card)
        db.clear_db()
