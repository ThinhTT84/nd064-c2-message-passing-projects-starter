from app.udaconnect.models import Location
from app.udaconnect.schemas import (
    LocationSchema,
)
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Location ingression API.")  # noqa

#Handle global exception
@api.errorhandler(Exception)
def handle_error(error):
    return {'message': str(error)}, 500

@api.route("/locations")
class LocationsResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        location: Location = LocationService.create(request.get_json())
        return location

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="path")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        print("GET location with location_id:", location_id)
        location: Location = LocationService.retrieve(location_id)
        return location