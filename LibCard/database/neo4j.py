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


def neo4j_tests():
    # Test Neo4j queries
    print("Test Neo4j queries")
    db = Neo4j()
    db.clear_db()

    # add and get
    print("Adding a card")
    db.add_card("17", Card("Goluboe salo", "Vladimir Sorokin", "1999", None))
    print(db.get_card("17"))

    # update
    print("Now it should be changed with a new date by updating")
    db.update_card("17", Card("Goluboe salo", "Vladimir Sorokin", "2000", None))
    print(db.get_card("17"))

    # add with same id
    print("Now it should return back its date by adding a new card with same id")
    db.add_card("17", Card("Goluboe salo", "Vladimir Sorokin", "1999", None))
    print(db.get_card("17"))

    # remove
    print("Let's remove it, we want to get None as result of search")
    db.remove_card("17")
    print(db.get_card("17"))

    #get max id
    print("Test get max id, it should be 87")
    db.add_card("13", Card("The Teachings of Don Juan", "C. Castaneda", "1968", None))
    db.add_card("87", Card("Hermit and Sixfinger", "V. Pelevin", "1990", None))
    print(db.get_max_id())

    #clear db
    print("Now we fuck up all data")
    db.clear_db()
    print(db.get_card("13"))
    print(db.get_card("87"))

    #is_empty
    print("is_empty must be true")
    print(db.is_empty())
    print("is_empty must be false")
    db.add_card("13", Card("The Teachings of Don Juan", "C. Castaneda", "1968", None))
    print(db.is_empty())


if __name__ == '__main__':
    neo4j_tests()