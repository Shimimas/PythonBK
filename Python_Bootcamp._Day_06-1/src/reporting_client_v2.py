import grpc
from recommendations_pb2_grpc import RecommendationsStub
from recommendations_pb2 import ForRequest
from google.protobuf.json_format import MessageToJson
import random
import json
from pydantic import BaseModel, validator
from typing import List, Dict, Optional

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


channel = grpc.insecure_channel("localhost:50051")
client = RecommendationsStub(channel)
while True:
    request = ForRequest(number=1)
    js = MessageToJson(client.GetShip(request))
    d = json.loads(js)
    print(d)
    try:
        User.parse_obj(d)
        print(d)
    except ValueError:
        pass
