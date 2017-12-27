from unittest import TestLoader, TextTestRunner, TestSuite
from database.neo4j import Neo4jTest
from database.memcached import MemcachedTest
from database.database_manager import DatabaseManagerTests
from database.mongo import MongoTest


def test_all():

    loader = TestLoader()
    suite = TestSuite((
        #loader.loadTestsFromTestCase(MongoTest),
        loader.loadTestsFromTestCase(MemcachedTest),
        #loader.loadTestsFromTestCase(Neo4jTest),
        #loader.loadTestsFromTestCase(DatabaseManagerTests),
    ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
