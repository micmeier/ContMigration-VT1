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

def write_random_data(collection_name, count, worker, port, state_file):
    client = pymongo.MongoClient(f"mongodb://{worker}:{port}")
    db = client["discRW"]
    collection = db[collection_name]
    print("MongoDb connected at: " + datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f"))
    print("---")

    # Read the state information from the file or start fresh
    try:
        with open(state_file, 'r') as f:
            state_info = f.read().split(',')

# if state.txt is avail -> migration
            if len(state_info) == 2:
                start_index, remaining_entries = map(int, state_info)
                count = remaining_entries
                start_index += 1

            else:
                start_index, remaining_entries = 0, count

# fresh start without state.txt
    except FileNotFoundError:
        start_index, remaining_entries = 0, count

    for i in range(start_index, start_index + count):
        data = generate_random_data(i)

        collection.update_one(
            {"key": data["key"]},
            {"$set": {"time": data["time"][0]}},
            upsert=True
        )

        print(f"{data} added to MongoDB")

        remaining_entries -= 1
        print(f"Remaining entries: {remaining_entries}")
        print(f"---")

        # Save the state information to the file for the next run
        with open(state_file, 'w') as f:
            f.write(f"{i},{remaining_entries}")

        # Sleep for one second between writes (we might have to delete/change)
        time.sleep(0.001)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <collection_name> <count> <worker:port> <state_file>")
        sys.exit(1)

    collection_name = sys.argv[1]
    count = int(sys.argv[2])
    worker_and_port = sys.argv[3].split(':')
    state_file = sys.argv[4]

    if len(worker_and_port) != 2:
        print("Invalid worker:port format")
        sys.exit(1)

    worker = worker_and_port[0]
    port = worker_and_port[1]

    write_random_data(collection_name, count, worker, port, state_file)
