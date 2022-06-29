import logging
import json
from typing import Dict

from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from flask import g

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-location-api")


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        logger.debug("Retrieving location with id %s", location_id)
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one_or_none()
        )
        
        if (location is None):
            logger.warning("Location with id %s not found", location_id)
            return None

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict):
        logger.debug("Creating location with data %s", location)
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        # produce kafka message
        kafka_data = json.dumps(location).encode()
        g.kafka_producer.send(g.kafka_location_topic, kafka_data)