import pymongo
from datetime import datetime
import sys
import time

def generate_random_data(i):
    random_data = {
        "key": i,
        "time": [datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")]
    }
    return random_data

def write_random_data(collection, key):
    data = generate_random_data(key)

    collection.update_one(
        {"key": data["key"]},
        {"$set": {"time": data["time"][0]}},
        upsert=True)

    print(f"{data} added to MongoDB at key {key}")
    print(f"---")

def get_last_key(collection):
    document = collection.find_one(sort=[("key", pymongo.DESCENDING)])
    if document:
        return document["key"]
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <worker> <port>")
        sys.exit(1)

    collection_name = "data"
    worker = sys.argv[1]
    port = sys.argv[2]

    client = pymongo.MongoClient(f"mongodb://{worker}:{port}")
    db = client["discRW"]
    collection = db[collection_name]

    print("MongoDb connected at: " + datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f"))
    print("---")

    key = get_last_key(collection) + 1

    try:
        while True:
            if key >=10000:
                break
            write_random_data(collection, key)
            key += 1
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    finally:
        client.close()
