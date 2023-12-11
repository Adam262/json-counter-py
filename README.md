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

_Note on exposed port_

The Python Flask web server runs on port 5000 by default. However, on current Mac OSX version, this port is taken by the AirPlay Server. You can see the process by running one of the below methods. So I exposed the Flask server to 5001 via Docker Compose.

```bash
❯ lsof -i :5000
COMMAND     PID       USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
ControlCe 39461 adambarcan    7u  IPv4 0x4f36ba550c588cb3      0t0  TCP *:commplex-main (LISTEN)
```

OR

```bash
 ❯ netstat -anv | grep 5000
tcp6       0      0  *.5000                 *.*                    LISTEN       131072  131072  39461      0 00100 00000006 0000000001f6b3c7 00000001 00000800      1      0 000001

❯ ps aux | grep 39461 | grep -v grep
adambarcan       39461   0.0  0.3 409849616  50352   ??  S    10:03PM   0:00.53 /System/Library/CoreServices/ControlCenter.app/Contents/MacOS/ControlCenter
```

#### /incr

This method increments a passed in key. The key must be a stringified integer between 0 and 9. If the key does not exist, it will be incremented to 1

_Body_
`'{ "key": "<KEY>"}'`, where KEY is an integer between 0 and 9

_Sample Request_
```
curl -X PUT \
  http://localhost:5001/incr \
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
  http://localhost:5001/decr \
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
  'http://localhost:5001/count?key=1' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json'


$ {"1":3,"error":""}
```

#### /ping
This method is a health check. It does not take query params

```
curl -X GET http://localhost:5001/ping

$ pong
```
