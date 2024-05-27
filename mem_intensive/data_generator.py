import redis
import random
from datetime import datetime
import sys
import time

def write_data(count):
    while count < 2000:
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")
        key = f"key_{count}"
        
        if redis_conn.exists(key):
            value = f"{current_time}"
        else:
            value = f"{current_time}"
        
        redis_conn.set(key, value)
        print(f"{value} set at key {count}")
        count += 1
       # time.sleep(1)

def get_last_key(redis_conn):
    keys = redis_conn.keys("key_*")

    if keys: 
        count = [int(key.split("_")[1]) for key in keys]
        return max(count)
    else: 
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Arg error")
        sys.exit(1)
    

    worker = sys.argv[1]
    port = sys.argv[2]
    
    redis_conn = redis.StrictRedis(host=worker, port=port, decode_responses=True)

    count = get_last_key(redis_conn) + 1
    write_data(count)
    
