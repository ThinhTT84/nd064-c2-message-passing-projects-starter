import json

from kafka import KafkaConsumer
from app.services import LocationService
from app.models import BaseModel
from app.session import DbSession


class LocationWorker():
    config = None
    def __init__(self, config):
        self.config = config

    def run(self, debug: bool = False):
        #To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(self.config.LOCATION_TOPIC_NAME, bootstrap_servers=self.config.KAFKA_SERVERS)

        #consume kafka message and create a new location
        for message in consumer:
            location = json.loads(message.value.decode('utf-8'))
            LocationService.create(location)

    
def create_app(env=None):
    from app.config import config_by_name

    config = config_by_name[env or "test"]
    app = LocationWorker(config)

    DbSession.init(config.SQLALCHEMY_DATABASE_URI)

    return app
