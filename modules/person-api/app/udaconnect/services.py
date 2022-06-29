import logging
from typing import Dict, List

from app.udaconnect.session import DbSession
from app.udaconnect.models import Person

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-person-api")

class PersonDbService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        with DbSession.session_scope() as session:
            session.add(new_person)
            session.commit()
            session.expunge_all()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        with DbSession.session_scope() as session:
            result = session.query(Person).get(person_id)
            session.expunge_all()
            return result

    @staticmethod
    def retrieve_all() -> List[Person]:
        with DbSession.session_scope() as session:
            result = session.query(Person).all()
            session.expunge_all()
            return result
