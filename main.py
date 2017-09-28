import memcache, neo4j.v1
import memcache, pymongo
mc = memcache.Client(['188.134.82.95:7005'], debug=0)
mc.set("default_message", "Hello World!")
print(mc.get("default_message"))


#neo4j test

driver = neo4j.v1.GraphDatabase.driver("bolt://localhost:7687", auth=neo4j.v1.basic_auth("neo4j", "neo4jdefpass"))
session = driver.session()

session.run("CREATE (a:Phrase {start: {start}, end: {end}})",
          {"start": "Hello, World!", "end": " by neo4j"})

result = session.run("MATCH (a:Phrase) WHERE a.start = {start} "
                   "RETURN a.start AS start, a.end AS end",
                   {"start": "Hello, World!"})
for record in result:
    print("%s %s" % (record["start"], record["end"]))

session.close()
# Pymongo hello world

client = pymongo.MongoClient("localhost", 27017)
db = client.test
print(db.name)
print(db.my_collection.insert_one({"x": 10}).inserted_id)
print(db.my_collection.insert_one({"x": 8}).inserted_id)
print(db.my_collection.insert_one({"x": 11}).inserted_id)
for item in db.my_collection.find():
    print(item["x"])
