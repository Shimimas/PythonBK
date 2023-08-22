from concurrent import futures
import random


import grpc

from recommendations_pb2 import (
    ShipRequest,
    Officers,
)

import recommendations_pb2_grpc

names = ['Normandy', 'Executor', 'Destroyer', 'Elephant', 'Mouse', 'T-34', 'Shadow', 'Mystery', 'SkyJet', 'Silense', 'Unknown']
of_names = ['Wolf', 'Bear', 'Fox', 'Eagle', 'Tiger', 'Lion', 'Ant', 'Outer', 'Fish', 'Cat']
of_s_names = ['Wild', 'Quite', 'Quick', 'Angry', 'Big', 'Little', 'Crazy', 'Smart', 'Unicum', 'Alone']
rank = ['Commander', 'Padavan', 'Master', 'Grandmaster', 'Younling']
class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def GetShip(self, request, context):
        alignment = random.randint(1, 2)
        if not alignment:
            name = names[random.randint(0, 9)]
        else:
            name = names[random.randint(0, 10)]
        class_ship = random.randint(1, 6)
        length = random.random() * 20000 + 1
        crew_size = random.randint(1, 500)
        armed = bool(random.randint(0, 1))
        sh_r = ShipRequest(alignment=alignment, name=name, classes=class_ship, length=length, crew_size=crew_size, armed=armed)
        if alignment == 1:
            amount = random.randint(1, 10)
        else:
            amount = random.randint(0, 10)
        for i in range(amount):
            of = Officers()
            of.first_name = of_names[random.randint(0, 9)]
            of.last_name = of_s_names[random.randint(0, 9)]
            of.rank = rank[random.randint(0, 4)]
            sh_r.officers.append(of)
        return sh_r
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()