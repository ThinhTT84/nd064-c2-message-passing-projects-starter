import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db, personService
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from sqlalchemy.sql import text

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-connection-api")


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[ConnectionSchema]:
        # Cache all users in memory for quick lookup
        person_map: Dict[str, PersonSchema] = {person.id: person for person in personService.get_all()}

        # Prepare arguments for queries
        data = {
                "person_id": person_id,
                "meters": meters,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
            }

        query = text(
            """
        SELECT  l1.person_id, l1.id, ST_X(l1.coordinate) xlat, ST_Y(l1.coordinate) xlong, l1.creation_time
        FROM    location l1, location l2
        WHERE   ST_DWithin(l1.coordinate::geography,ST_SetSRID(l2.coordinate::geography,4326)::geography, :meters)
        AND     l1.person_id != l2.person_id
        AND     l2.person_id  = :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= l1.creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > l1.creation_time
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= l2.creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > l2.creation_time;
        """
        )
        result: List[ConnectionSchema] = []

        rows = db.engine.execute(query, data)
        
        for row in rows:
            logger.debug(f"Found connection: {row} ")

            location = LocationSchema()
            location.id= row["id"]
            location.person_id=row["person_id"]
            location.creation_time= row["creation_time"]
            location.latitude=row["xlat"]
            location.longitude=row["xlong"]

            connection = ConnectionSchema()
            connection.location = location
            connection.person = person_map[location.person_id]

            result.append(connection)

        return result