import redis
import random
from datetime import datetime


# Connect to Redis
redis_host = "worker1"
redis_port = 30569
redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def write_data(i):
    for j in range(i):
        time = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")
        key = f"key_{j}"
        
        if redis_conn.exists(key):
            existing_val = redis_conn.get(key)
            value = f"{existing_val}, {time}"
        else:
            value = f"{time}"
        
        redis_conn.set(key, value)
        print(f"{value} set at key {j}")

count = 100000000
write_data(count)
print("Redis job finished.")
