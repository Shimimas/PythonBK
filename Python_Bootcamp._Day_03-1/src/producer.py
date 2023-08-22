import json
import random
import redis

def prod():
    from_num = random.randint(1000000000, 9999999999)
    to_num = random.randint(1000000000, 9999999999)
    amount = random.randint(-1000000000, 1000000000)
    d = {
        "metadata": {
            "from": from_num,
            "to": to_num
        },
        "amount": amount
    }
    return json.dumps(d)

red = redis.Redis(host='localhost', port=6379, db=0)

def stream():
    red.publish('queue', prod())

if __name__ == "__main__":
    while True:
        stream()