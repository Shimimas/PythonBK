import grpc
from recommendations_pb2_grpc import RecommendationsStub
from recommendations_pb2 import ForRequest
from google.protobuf.json_format import MessageToJson
import random

channel = grpc.insecure_channel("localhost:50051")
client = RecommendationsStub(channel)
for i in range(random.randint(1, 10)):
    request = ForRequest(number=1)
    print(str(MessageToJson(client.GetShip(request))).replace('classes', 'class').replace('crewSize', 'crew_size'))