import redis

R = redis.Redis('localhost')

print (R.smembers('random:ip:found'))
