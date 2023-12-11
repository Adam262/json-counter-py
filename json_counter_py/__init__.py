from flask import Flask, request
from redis import Redis
VALID_KEYS=[str(x) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]

app = Flask(__name__)
r = Redis(host='redis', port=6379, decode_responses=True,password=None)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/incr", methods=['PUT'])
def incr():
    key = request.get_json()['key']
    if key not in VALID_KEYS:
        return {
            key: "",
            'error': "key must be an integer between 0 and 9"
        }
    incr = r.incr(key)
    return {
        key: incr,
        'error': None
    }

@app.route("/decr", methods=['PUT'])
def decr():
    key = request.get_json()['key']
    if key not in VALID_KEYS:
        return {
            key: "",
            'error': "key must be an integer between 0 and 9"
        }
    decr = r.decr(key)
    return {
        key: decr,
        'error': None
    }

@app.route("/count")
def count():
    key = request.args.get('key', '')
    if key not in VALID_KEYS:
        return {
            key: "",
            'error': "key must be an integer between 0 and 9"
        }
    return {
        key: r.get(key),
        'error': None
    }
