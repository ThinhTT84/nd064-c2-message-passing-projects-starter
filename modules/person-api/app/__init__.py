from concurrent import futures
import grpc
import person_pb2_grpc

from app.udaconnect.models import BaseModel
from app.udaconnect.session import DbSession
from app.udaconnect.personServicer import PersonServicer

class GrpcServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        person_pb2_grpc.add_PersonServiceServicer_to_server(
            PersonServicer(), self.server
        )
        self.server.add_insecure_port("[::]:50051")

    def startServer(self):
        self.server.start()
        self.server.wait_for_termination()

def create_app(env=None):
    from app.config import config_by_name

    app = GrpcServer()
    config = config_by_name[env or "test"]
    DbSession.init(config.SQLALCHEMY_DATABASE_URI)

    return app
