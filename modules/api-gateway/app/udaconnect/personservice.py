from typing import Dict, List
from app.udaconnect.schemas import PersonSchema

import grpc
import person_pb2_grpc
import person_pb2


class PersonService():


    config = None
    def init_config(self, config):
        self.config = config

    @staticmethod
    def Convert(person: person_pb2.Person) -> PersonSchema:
        result = PersonSchema()
        result.id = person.id
        result.first_name = person.first_name
        result.last_name = person.last_name
        result.company_name = person.company_name
        return result

    def retrieve_all(self) -> List[PersonSchema]:
        persons = []
        with grpc.insecure_channel(self.config.PERSON_API_HOST) as channel:
            client = person_pb2_grpc.PersonServiceStub(channel)
            response = client.GetAll(person_pb2.Empty())

            for person in response.items:
                persons.append(PersonService.Convert(person))
            
            return persons

    def create(self, person: Dict) -> PersonSchema:
        grpcRequest = person_pb2.CreatePersonRequest(
            first_name=person["first_name"], 
            last_name=person["last_name"], 
            company_name=person["company_name"])

        with grpc.insecure_channel(self.config.PERSON_API_HOST) as channel:
            client = person_pb2_grpc.PersonServiceStub(channel)
            response = client.Create(grpcRequest)
            return PersonService.Convert(response)

    def retrieve(self, person_id: int) -> PersonSchema:
        with grpc.insecure_channel(self.config.PERSON_API_HOST) as channel:
            client = person_pb2_grpc.PersonServiceStub(channel)
            response = client.Get(person_pb2.GetPersonRequest(id=person_id))
            return PersonService.Convert(response)