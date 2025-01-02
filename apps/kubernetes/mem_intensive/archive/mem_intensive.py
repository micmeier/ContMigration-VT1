import redis
import random
import datetime

# Connect to Redis
redis_host = "localhost"
redis_port = 6379
redis_password = ""
redis_db = 0
redis_conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)

# Write 1000 random key-value pairs into Redis
for i in range(1000):
    key = f"key_{i}"
    value = f"value_{i}"
    redis_conn.set(key, value)
    
# Print all keys to the terminal
keys = redis_conn.keys()
for key in keys:
    print("---ALL KEYS SET---")
    print(key)
    print("---")    

# When 1000 pairs are reached, randomly choose a key from the previous step and change its value
for i in range(1001, 1000000):
    key = f"key_{random.randint(0, 999)}"
    value = f"value_{i}"
    redis_conn.set(key, value)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    start_time = datetime.datetime(1970, 1, 1)
    timestamp_ms = int((datetime.datetime.now() - start_time).total_seconds() * 1000)
    print(f"Key: {key}, New Value: {value}, Timestamp: {timestamp}, Timestamp (ms): {timestamp_ms}")
