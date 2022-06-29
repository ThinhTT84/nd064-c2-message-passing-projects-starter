- Person API using gRPC
- Get all person `GetAll(Empty)` returns `PersonList`
- Get specific person by id `Get(GetPersonRequest)` returns `Person`
- Create a person `Create(CreatePersonRequest)` returns new created `Person`

```proto3
syntax = "proto3";

message Person {
    int32 id = 1;
    string first_name = 2;
    string last_name = 3;
    string company_name = 4;
}


message PersonList {
    repeated Person items = 1;
}


message Empty {
}

message CreatePersonRequest {
    string first_name = 1;
    string last_name = 2;
    string company_name = 3;
}

message GetPersonRequest {
    int32 id = 1;
}

service PersonService {
    rpc GetAll(Empty) returns (PersonList);
    rpc Get(GetPersonRequest) returns (Person);
    rpc Create(CreatePersonRequest) returns (Person);
}
```