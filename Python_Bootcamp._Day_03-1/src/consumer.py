import redis
import logging
import sys
import json

def user_counter():
    sub = red.pubsub()
    sub.subscribe('queue')
    for message in sub.listen():
        if message is not None and isinstance(message, dict):
            if isinstance(message['data'], str):
                data = json.loads(message['data'])
                if data['metadata']['to'] in bad_numbers and data['metadata']['amount'] >= 0:
                    data['metadata']['to'], data['metadata']['from'] = data['metadata']['from'], data['metadata']['to']
                logging.info(data)

logging.basicConfig(format = '%(message)s', level=logging.INFO)
bad_numbers = set()
if len(sys.argv) >= 3:
    input_string = sys.argv[2].replace(',', ' ').split()
    for el in input_string:
        bad_numbers.add(int(el))

red = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
while True:
  user_counter()