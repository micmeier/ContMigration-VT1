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

def write_random_data(collection_name, worker, port):
    client = pymongo.MongoClient(f"mongodb://{worker}:{port}")
    db = client["discRW"]
    collection = db[collection_name]
    print("MongoDb connected at: " + datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f"))
    print("---")
    key = 0

    while True:
        data = generate_random_data(key)

        collection.update_one(
            {"key": data["key"]},
            {"$set": {"time": data["time"][0]}},
            upsert=True)

        key += 1
        print(f"{data} added to MongoDB at key {key}")
        print(f"---")
	    
        # Sleep for one second between writes (we might have to delete/change)
        time.sleep(1)




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <worker> <port>")
        sys.exit(1)

    collection_name = "data"
    worker = sys.argv[1]
    port = sys.argv[2]

    write_random_data(collection_name, worker, port)
