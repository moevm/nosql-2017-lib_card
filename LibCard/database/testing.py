from database.neo4j import neo4j_tests
from database.memcached import memcached_tests
from database.database_manager import database_manager_tests


def test_all():
    database_manager_tests()
    neo4j_tests()
    memcached_tests()
