from pymongo import MongoClient

client = MongoClient('mongodb://mongodb-service-cluster.mongo:27017/')
db = client.mydb
collection = db.test

for i in range(1000):
    collection.insert_one({'x': i})

cursor = collection.find()
for document in cursor:
    print(document)
