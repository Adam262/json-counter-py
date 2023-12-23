from redis import Redis
r = Redis(host='redis', port=6379, decode_responses=True,password=None)

def redis_incr(key):
    return r.incr(key)

def redis_decr(key):
    return r.decr(key)

def redis_get(key):
    return r.get(key)

