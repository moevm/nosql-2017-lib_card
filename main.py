import neo4j.v1
from pymongo import MongoClient
from memcache import Client as MemcacheClient

ip = '188.134.82.95'
mc_port = 7005
neo4j_port = 7007
mongo_port = 7009

# memcached test

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
