import redis

rclient = redis.Redis(host='redis', port=6379, db=0)