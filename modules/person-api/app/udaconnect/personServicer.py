from typing import List

from app.udaconnect.services import PersonDbService
import app.udaconnect.models as models

import person_pb2
import person_pb2_grpc


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    
    def Convert(self, person: models.Person, context) -> person_pb2.Person:
        result = person_pb2.Person()
        result.id = person.id
        result.first_name = person.first_name
        result.last_name = person.last_name
        result.company_name = person.company_name
        return result

    def Get(self, request, context):
        person: models.Person = PersonDbService.retrieve(request.id)
        return self.Convert(person, context)

    def GetAll(self, request, context):
        all_person: List[models.Person] = PersonDbService.retrieve_all()
        result = person_pb2.PersonList()
        for person in all_person:
            result.items.append(self.Convert(person, context))
        return result

    def Create(self, request, context):
        request_value = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name,
        }

        new_person: models.Person = PersonDbService.create(request_value)
        return self.Convert(new_person, context)
