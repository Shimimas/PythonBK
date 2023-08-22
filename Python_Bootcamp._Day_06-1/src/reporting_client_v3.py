import psycopg2
import grpc
from recommendations_pb2_grpc import RecommendationsStub
from recommendations_pb2 import ForRequest
from google.protobuf.json_format import MessageToJson
import json
from pydantic import BaseModel, validator
from typing import List, Dict, Optional
import sys

str1 = '\''
str2 = '\'\''

class User(BaseModel):
    name: str
    classes: str
    length: float
    crewSize: int
    armed: bool = False
    officers: Optional[List[Dict[str, str]]]
    alignment: str

    @validator('classes')
    def n8(cls, v):
        return v

    @validator('alignment')
    def n4(cls, v, values):
        if values['classes'] == 'Destroyer' or values['classes'] == 'Destroyer':
            if v == 'Enemy':
                raise ValueError()
        return v

    @validator('length')
    def n1(cls, v, values):
        if values['classes'] == 'Corvette':
            if 80 <= v <= 250:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Frigate':
            if 300 <= v <= 600:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Cruiser':
            if 500 <= v <= 1000:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Destroyer':
            if 800 <= v <= 2000:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Aircraft_Carrier':
            if 1000 <= v <= 4000:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Dreadnought':
            if 5000 <= v <= 20000:
                return v
            else:
                raise ValueError()
            
    @validator('crewSize')
    def n2(cls, v, values):
        if values['classes'] == 'Corvette':
            if 4 <= v <= 10:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Frigate':
            if 10 <= v <= 15:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Cruiser':
            if 15 <= v <= 30:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Destroyer':
            if 50 <= v <= 80:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Aircraft_Carrier':
            if 120 <= v <= 250:
                return v
            else:
                raise ValueError()
        elif values['classes'] == 'Dreadnought':
            if 300 <= v <= 500:
                return v
            else:
                raise ValueError()
            
    @validator('armed')
    def n3(cls, v, values):
        if values['classes'] == 'Aircraft_Carrier' and v:
            raise ValueError()
        else:
            return v

if sys.argv[1] == 'scan':
    channel = grpc.insecure_channel("localhost:50051")
    client = RecommendationsStub(channel)
    oficers_enemy = set()
    oficers_ally = set()
    adding_db = set()
    while True:
        conn = psycopg2.connect(dbname="selectel", user="selectel", password="selectel", host="127.0.0.1", port="5432")
        cursor = conn.cursor()
        request = ForRequest(number=1)
        js = MessageToJson(client.GetShip(request))
        d = json.loads(js)
        if 'armed' not in d:
            d['armed'] = False
        if 'officers' not in d:
            d['officers'] = []
        try:
            User.parse_obj(d)
            if (str(d['officers']), d['name']) not in adding_db:
                print(d)
                adding_db.add((str(d['officers']), d['name']))
                cursor.execute(f"INSERT INTO ships (alignment, name, classes, length, crewSize, armed, officers) VALUES ('{d['alignment']}', '{d['name']}', '{d['classes']}', {d['length']}, {d['crewSize']}, {d['armed']}, '{str(d['officers']).replace(str1, str2)}')")
                conn.commit()
                for el in d['officers']:
                    print('el = ', el)
                    print('oficers_ally = ', oficers_ally)
                    print('oficers_enemy = ', oficers_enemy)
                    if d['alignment'] == "Enemy":
                        if (el['firstName'], el['lastName'], el['rank']) in oficers_ally:
                            cursor.execute(f"INSERT INTO traitors (first_name, last_name, rank) VALUES ('{el['firstName']}', '{el['lastName']}', '{el['rank']}')")
                            conn.commit()
                        oficers_enemy.add((el['firstName'], el['lastName'], el['rank']))
                    else:
                        if (el['firstName'], el['lastName'], el['rank']) in oficers_enemy:
                            cursor.execute(f"INSERT INTO traitors (first_name, last_name, rank) VALUES ('{el['firstName']}', '{el['lastName']}', '{el['rank']}')")
                            conn.commit()
                        oficers_ally.add((el['firstName'], el['lastName'], el['rank']))
        except ValueError:
            pass
        cursor.close()
        conn.close()
elif sys.argv[1] == 'list_traitors':
    conn = psycopg2.connect(dbname="selectel", user="selectel", password="selectel", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM traitors")
    print(cursor.fetchall())
    cursor.close()
    conn.close()
else:
    conn = psycopg2.connect(dbname="selectel", user="selectel", password="selectel", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ships")
    print(cursor.fetchall())
    cursor.close()
    conn.close()