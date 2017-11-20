import neo4j.v1
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection as MongoCollection
from memcache import Client as MemcacheClient
from typing import Tuple, Dict, List
from bottle import route, run, static_file


class Network:

    ip = '188.134.82.95'
    memcached_port = 7005
    neo4j_port = 7007
    mongo_port = 7009


class DatabaseName:
    TYPE = str
    MEMCACHED = 'memcached'
    MONGODB = 'mongo db'
    NEO4J = 'neo4j'


class HistoryRecord:

    def __init__(self, reader: str, date_from: str, date_to: str):
        self.reader = reader
        self.date_from = date_from
        self.date_to = date_to

    @staticmethod
    def create_from_list(obj: List[Dict[str, str]]):
        return [HistoryRecord(i['reader'], i['from'], i['to']) for i in obj] if obj else None


class Card:

    def __init__(self, title: str, author: str, year: str, history: List[HistoryRecord]):
        self.title = title
        self.author = author
        self.year = year
        self.history = history

    def __str__(self):
        return f'Card({self.title} {self.author} {self.year})'

    @staticmethod
    def create_from_dict(obj):
        return Card(obj['title'], obj['author'], obj['year'], HistoryRecord.create_from_list(obj['history']))


class TempDatabase:

    def __init__(self):
        pass


class Database:

    def __init__(self, client, type):
        self.client = client
        self.type = type

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

    def save(self):
        pass


class Memcached(Database):

    def __init__(self, ip=Network.ip, port=Network.memcached_port):
        super().__init__(MemcacheClient([f'{ip}:{port}'], debug=0), DatabaseName.MEMCACHED)
        self.client: MemcacheClient

    def add_card(self, id_: str, card: Card):
        self.client.set(id_, {'title': card.title, 'author': card.author, 'year': card.year, 'history': None})

    def get_card(self, id_):
        return Card.create_from_dict(self.client.get(id_))


class Neo4j(Database):

    def __init__(self, ip=Network.ip, port=Network.neo4j_port):
        session = neo4j.v1.GraphDatabase.driver(f"bolt://{ip}:{port}",
                                                auth=neo4j.v1.basic_auth("neo4j", "pineo4j"))
        super().__init__(session, DatabaseName.NEO4J)
        self.client: neo4j.v1.Driver

    def create_temp_db(self) -> TempDatabase:
        pass

    def load_from_temp_db(self, database: TempDatabase):
        pass

    def clear_db(self):
        with self.client.session() as session:
            session.run("MATCH (node) DETACH DELETE node")

    def add_card(self, id_: str, card: Card):
        query: str = """MERGE (card:Card {id: {id_}, histoty: "null"})
                       MERGE (book:Book {title: {title}, year: {year}, author: {author}})
                       MERGE (card)-[:ASSOCIATED_WITH]-(book)"""
        args: dict = {"id_": id_, "title": card.title, "year": card.year, "author": card.author}
        with self.client.session() as session:
            session.run(query, args)

    def remove_card(self, id_):
        query: str = "MATCH (book:Book)-[rel:ASSOCIATED_WITH]-(card:Card {id: {id_}}) DELETE card, rel"
        args: dict = {"id_": id_}
        with self.client.session() as session:
            session.run(query, args)

    def update_card(self, id_, card: Card):
        query: str = "MATCH (card:Card {id: {id_}})-[]-(book:Book) " \
                     "SET book.title = {title}, book.author = {author}, book.year = {year}"
        args: dict = {"id_": id_, "title": card.title, "author": card.author, "year": card.year}
        with self.client.session() as session:
            session.run(query, args)

    def get_card(self, id_):
        query: str = """MATCH (card:Card {id: {id_}})--(book: Book)
                    RETURN book.title AS title, book.author AS author, book.year AS year, card.history AS history"""
        args: dict = {"id_": id_}
        with self.client.session() as session:
            result: neo4j.v1.BoltStatementResult = session.run(query, args)
            records: list = result.data()
            if len(records) == 0:
                return None
            return Card.create_from_dict(records[0])


class MongoDB(Database):

    def __init__(self, ip=Network.ip, port=Network.mongo_port):
        client = MongoClient(ip, port)
        super().__init__(client.library.my_collection, DatabaseName.MONGODB)

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


class DatabaseManager:

    def __init__(self):
        self._memcached = Memcached()
        self._neo4j = Neo4j()
        self._mongodb = MongoDB()

        self._curr_db: Database = self._memcached

    def switch_to_database(self, database: DatabaseName.TYPE):

        temp_db: TempDatabase = self._curr_db.create_temp_db()
        old_db: Database = self._curr_db

        if database == DatabaseName.MEMCACHED:
            self._curr_db = self._memcached

        elif database == DatabaseName.MONGODB:
            self._curr_db = self._mongodb

        elif database == DatabaseName.NEO4J:
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

    def get_card(self, id_):
        return self._curr_db.get_card(id_)


db: DatabaseManager = DatabaseManager()
db.add_card("2", "Test title", "Artur", "2k17")
json = db.get_card("2")
print('memcached:', json)

db.switch_to_database(DatabaseName.MONGODB)
db.add_card("2", "Test title", "Artur", "2k17")
json = db.get_card("2")
print('mongodb:', json)

db.switch_to_database(DatabaseName.NEO4J)
db.add_card("2", "Test title", "Artur", "2k17")
json = db.get_card("2")
print('neo4j:', json)

#Test Neo4j queries
print("Test Neo4j queries")
db.clear_db()

#add and get
print("Adding a card")
db.add_card("17", "Goluboe salo", "Vladimir Sorokin", "1999")
print(db.get_card("17"))

#update
print("Now it should be changed with a new date by updating")
db.update_card("17", "Goluboe salo", "Vladimir Sorokin", "2000")
print(db.get_card("17"))

#add with same id
print("Now it should return back its date by adding a new card with same id")
db.add_card("17", "Goluboe salo", "Vladimir Sorokin", "1999")
print(db.get_card("17"))

#remove
print("Let's remove it, we want to get None as result of search")
db.remove_card("17")
print(db.get_card("17"))

#clear db
print("Now we push two new cards and fuck up all data")
db.add_card("13", "The Teachings of Don Juan", "C. Castaneda", "1968")
db.add_card("87", "Hermit and Sixfinger", "V. Pelevin", "1990")
db.clear_db()
print(db.get_card("13"))
print(db.get_card("87"))

#it's too sad when you don't know how to use unit tests

@route('/')
def index():
    return static_file('index.html', root='html')


@route('/<img:re:favicon.ico>')
@route('/img/<img:path>')
def img_serve(img):
    return static_file(img, root='html/img')


# for css files
@route('/static/<file:path>')
def static_serve(file):
    return static_file(file, root='html/static')


run(host='127.0.0.1', port=80)


# memcached test
'''
mc = MemcacheClient([f'{ip}:{mc_port}'], debug=0)
print(mc.get("default_message"))

# neo4j test

driver = neo4j.v1.GraphDatabase.driver(f"bolt://{ip}:{neo4j_port}", auth=neo4j.v1.basic_auth("neo4j", "pineo4j"))
session = driver.session()

result = session.run("MATCH (a:Phrase) WHERE a.start = {start} "
                     "RETURN a.start AS start, a.end AS end",
                     {"start": "Hello, World!"})

for record in result:
    print("%s %s" % (record["start"], record["end"]))

session.close()

# Pymongo hello world

client = MongoClient(ip, mongo_port)
db = client.test
for item in db.my_collection.find():
    print(item["hello world"])
'''