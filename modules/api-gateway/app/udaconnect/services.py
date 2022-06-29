import logging
from datetime import datetime
from typing import Dict, List

from app.udaconnect.schemas import ConnectionSchema, LocationSchema
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api")

DATE_FORMAT = "%Y-%m-%d"

class ConnectionService():
    config = None
    def init_config(self, config):
        self.config = config

    def find_contacts(self, person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[ConnectionSchema]:

        uri = f"{self.config.CONNECTION_API_BASE_URL}/persons/{person_id}/connection"
        resp = requests.get(uri, params={"start_date": start_date.strftime(DATE_FORMAT), "end_date": end_date.strftime(DATE_FORMAT), "meters": meters})
        
        connections = []

        for connection in resp.json():
            logger.debug(f"Found connection: {connection} ")
            connections.append(ConnectionSchema().load(connection))
        
        return connections


class LocationService():
    config = None
    def init_config(self, config):
        self.config = config

    def retrieve(self, location_id) -> LocationSchema:
        uri = f"{self.config.LOCATION_API_BASE_URL}/locations/{location_id}"
        resp = requests.get(uri)
        location = LocationSchema().load(resp.json())
        return location

    def create(self, location: Dict) -> LocationSchema:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        uri = f"{self.config.LOCATION_API_BASE_URL}/locations"
        resp = requests.post(uri, json=location)
        new_location = LocationSchema().load(resp.json())
        return new_location