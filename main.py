import memcache, pymongo
mc = memcache.Client(['188.134.82.95:7005'], debug=0)
mc.set("default_message", "Hello World!")
print(mc.get("default_message"))

# Pymongo hello world

client = pymongo.MongoClient("localhost", 27017)
db = client.test
print(db.name)
print(db.my_collection.insert_one({"x": 10}).inserted_id)
print(db.my_collection.insert_one({"x": 8}).inserted_id)
print(db.my_collection.insert_one({"x": 11}).inserted_id)
for item in db.my_collection.find():
    print(item["x"])
