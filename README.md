## json counter

### Task
* Write a program which delivers a working stateful network server which handles traffic over HTTP and
receives JSON input and output

* The request from the client will contain a single integer, and the output from one endpoint should be the number of times that the number has been sent to the server before. For example, if I send “1” to the server once, when I get a response, it should indicate that “1” has been seen once. 

* For fun, added a decrement endpoint

### Design Decision

* A simple Web server written in Python. I already did this project in Golang + Ruby, so wanted to learn some Python.

* Store data in Redis with key/value schema:

```
KEY: INCREMENTED_COUNT integer
```

* Orchestrate as docker compose

### Dependencies

* [Docker Desktop](https://www.docker.com/get-started)
* [asdf](https://asdf-vm.com/#/) version manager (for local development only)

### Getting Started

Web server image is publicly available on [Dockerhub](https://hub.docker.com/r/adam262/json-counter-sinatra)

To run the project, git clone this repo and run below command from repo:

```
docker-compose up --build -d
docker-compose logs -f
```

To stop project

```
docker-compose down
```

### API

#### /incr

This method increments a passed in key. The key must be a stringified integer between 0 and 9. If the key does not exist, it will be incremented to 1

_Body_
`'{ "key": "<KEY>"}'`, where KEY is an integer between 0 and 9

_Sample Request_
```
curl -X PUT \
  http://localhost:5000/incr \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "key": "1" }'

$ {"1":4,"error":""}
$
```

#### /decr

This method decrements a passed in key. The key must be a stringified integer between 0 and 9. If the key does not exist, it will be incremented to -1

_Body_
`'{ "key": "<KEY>"}'`, where KEY is an integer between 0 and 9

_Sample Request_
```
curl -X PUT \
  http://localhost:5000/decr \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "key": "1" }'

$ {"1":4,"error":""}
$
```

#### /count

This method returns the current count of a passed in key, based on prior increments. The key must be a stringified integer between 0 and 9. If the key is valid but does not exist in the database, it will be returned as 0.

_Query Params_
`?key=KEY`, where KEY is an integer between 0 and 9

```
curl -X GET \
  'http://localhost:5000/count?key=1' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json'


$ {"1":3,"error":""}
```

#### /ping
This method is a health check. It does not take query params

```
curl -X GET http://localhost:5000/ping

$ pong
```
