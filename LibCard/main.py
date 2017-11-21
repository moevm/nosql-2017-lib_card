from database.routing import run_server
from database.neo4j import neo4j_tests
from database.database_manager import database_manager_tests


def do_testing():
    database_manager_tests()
    neo4j_tests()


if __name__ == '__main__':
    do_testing()
    run_server()


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