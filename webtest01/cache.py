#-*- coding: utf-8 -*-

import redis
from conf import conf

class Cache():
    def __init__(self):
        self.rds = redis.Redis(host=conf.redis_ip, port=conf.redis_port, db=conf.redis_db, password=conf.redis_password)
    def incr(self, key, num=1):
        return self.rds.incr(key, num)

    def get(self, key):
        r   = self.rds.get(key)
        return r
    def set(self, key, val):#, t=conf.redis_timeout):
        r   = self.rds.set(key, val)#, t)
    def del_(self, key):
        r   = self.rds.delete(key)
    def hget(self, name, key):
        r   = self.rds.hget(name, key)
        return r
    def hset(self, name, key, val):
        r   = self.rds.hset(name, key, val)
        return r
    def flushall(self):
        r = self.rds.flushall()
    def gets(self, pat):
        keys = self.keys(pat)
        values = self.values(keys)
        return zip(keys, values)

    def keys(self, pat):
        return self.rds.keys(pattern=pat)
    def values(self, keys):
        with self.rds.pipeline(transaction=False) as p:
            for e in keys:
                p.get(e)
            return p.execute()

cache = Cache()

if __name__ == '__main__':
    r = cache.flushall()
    z = zip(['a1', 'a2', 'a3', 'a4'], ['b1', 'b2', 'b3', 'b4'])
    for e in z:
        cache.set(e[0], e[1])
    k = 'a*'
    for k, v in cache.gets(k):
        print(k)
        print(v)
