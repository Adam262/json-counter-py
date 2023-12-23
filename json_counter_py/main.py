from flask import Flask, request
from json_counter_py.db_redis import redis_incr, redis_decr, redis_get

app = Flask(__name__)

VALID_KEYS=[str(x) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]

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
    val_incr = redis_incr(key)
    return {
        key: val_incr,
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
    val_decr = redis_decr(key)
    return {
        key: val_decr,
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
        key: redis_get(key),
        'error': None
    }
