from datetime import datetime
import logging

from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)

from flask import request, g
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa
logger = logging.getLogger("udaconnect-api-gateway")


#Handle global exception
@api.errorhandler(Exception)
def handle_error(error):
    logger.error(error)
    return {'message': str(error)}, 500


@api.route("/locations")
class LocationsResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> LocationSchema:
        request.get_json()
        return g.locationService.create(request.get_json())

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in = "path") 
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> LocationSchema:
        return g.locationService.retrieve(location_id)


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> PersonSchema:
        payload = request.get_json()
        return g.personService.create(payload)

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[PersonSchema]:
        persons: List[PersonSchema] = g.personService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="path")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> PersonSchema:
        person: PersonSchema = g.personService.retrieve(int(person_id))
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = g.connectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
