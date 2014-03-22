import redis

R = redis.Redis('localhost')

i = R.smembers('random:ip:found')

for n in i:
	print(n, R.hgetall('random:'+n))

