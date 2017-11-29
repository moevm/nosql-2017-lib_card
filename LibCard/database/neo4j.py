import unittest
from database.network import server_ip, neo4j_port
from database.database import *
from database.card import Card
import neo4j.v1


class Neo4j(Database):

    def __init__(self, ip=server_ip, port=neo4j_port):
        session = neo4j.v1.GraphDatabase.driver(f"bolt://{ip}:{port}",
                                                auth=neo4j.v1.basic_auth("neo4j", "pineo4j"))
        super().__init__(session, NEO4J)
        self.client: neo4j.v1.Driver

    def clear_db(self):
        with self.client.session() as session:
            session.run("MATCH (node) DETACH DELETE node")

    def add_card(self, id_: str, card: Card):
        query: str = """MERGE (card:Card {id: {id_}, history: "null", image: {image}})
                       MERGE (book:Book {title: {title}, year: {year}, author: {author}})
                       MERGE (card)-[:ASSOCIATED_WITH]-(book)"""
        args: dict = {"id_": id_,
                      "title": card.title,
                      "year": card.year,
                      "author": card.author,
                      "image": card.image if card.image else 'null'}
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
        args: dict = {"id_": id_,
                      "title": card.title,
                      "author": card.author,
                      "year": card.year}
        with self.client.session() as session:
            session.run(query, args)

    def get_card(self, id_) -> Card:
        query: str = """MATCH (card:Card {id: {id_}})--(book: Book)
                    RETURN book.title AS title, book.author AS author, book.year AS year, card.history AS history, card.image AS image"""
        args: dict = {"id_": id_}
        with self.client.session() as session:
            result: neo4j.v1.BoltStatementResult = session.run(query, args)
            records: list = result.data()
            if len(records) == 0:
                return None
            return Card.create_from_dict({k: (records[0][k] if records[0][k] != 'null'
                                              else None) for k in records[0]})

    def get_max_id(self) -> int:
        query = "MATCH (card:Card) RETURN card.id AS id ORDER BY card.id DESC LIMIT 1"
        with self.client.session() as session:
            result: neo4j.v1.BoltStatementResult = session.run(query)
            records: list = result.data()
            if len(records) == 0:
                return 0
            return int(records[0]["id"])

    def is_empty(self) -> bool:
        query = "MATCH (card:Card) RETURN card IS NULL AS isEmpty LIMIT 1"
        with self.client.session() as session:
            result: neo4j.v1.BoltStatementResult = session.run(query)
            records: list = result.data()
            if len(records) == 0:
                return True
            return bool(records[0]["isEmpty"])

    def get_all_keys(self) -> List[str]:
        query = "MATCH (card:Card) RETURN card.id AS id"
        with self.client.session() as session:
            result: neo4j.v1.BoltStatementResult = session.run(query)
            records: list = result.data()
            ids: List[str] = []
            for record in records:
                ids += [record["id"]]
            return ids


class Neo4jTest(unittest.TestCase):
    def test_add_and_get(self):
        neo4j = Neo4j()
        card = Card('Vova007', 'Artur', '2k17', None, None)
        neo4j.add_card('1', card)
        self.assertIsInstance(neo4j.get_card('1'), Card)
        neo4j.clear_db()

    def test_update(self):
        neo4j = Neo4j()
        card = Card('Vova007', 'Artur', '2k17', None, None)
        neo4j.add_card('1', card)
        old_card = neo4j.get_card('1')
        old_card_tuple = (old_card.title, old_card.author, old_card.year, old_card.history)
        card_for_update = Card('Spica', 'Spicin', '1980', None, None)
        neo4j.update_card('1', card_for_update)
        updated_card = neo4j.get_card('1')
        new_card_tuple = (updated_card.title, updated_card.author,updated_card.year, updated_card.history)
        self.assertNotEqual(old_card_tuple, new_card_tuple, 'Comparing old and new cards')
        neo4j.clear_db()

    def test_remove(self):
        neo4j = Neo4j()
        card = Card('Vova007', 'Artur', '2k17', None, None)
        neo4j.add_card('1', card)
        neo4j.remove_card('1')
        search_result = neo4j.get_card('1')
        self.assertIsNone(search_result)
        neo4j.clear_db()

    def test_get_max_id(self):
        neo4j = Neo4j()
        firstCard = Card('Vova007', 'Artur', '2k17', None, None)
        secondCard = Card('Vova007', 'Artur', '2k17', None, None)
        thirdCard = Card('Vova007', 'Artur', '2k17', None, None)
        neo4j.add_card('2',firstCard)
        neo4j.add_card('3', secondCard)
        neo4j.add_card('4', thirdCard)
        self.assertEqual(neo4j.get_max_id(), 4)
        neo4j.clear_db()

    def test_clear_db(self):
        neo4j = Neo4j()
        neo4j.clear_db()
        self.assertEqual(neo4j.is_empty(), True)

    def test_is_empty(self):
        neo4j = Neo4j()
        card = Card('Vova007', 'Artur', '2k17', None, None)
        neo4j.add_card('1', card)
        self.assertEqual(neo4j.is_empty(), False)
        neo4j.clear_db()
        self.assertEqual(neo4j.is_empty(), True)

    def test_get_all_cards(self):
        neo4j = Neo4j()
        firstCard = Card('Vova007', 'Artur', '2k17', None, None)
        secondCard = Card('Vova007', 'Artur', '2k17', None, None)
        thirdCard = Card('Vova007', 'Artur', '2k17', None, None)
        neo4j.add_card('2', firstCard)
        neo4j.add_card('3', secondCard)
        neo4j.add_card('4', thirdCard)
        self.assertEqual(neo4j.get_all_keys(), ['2', '3', '4'])
        neo4j.clear_db()
