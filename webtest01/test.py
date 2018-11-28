import time
import json
from cache import cache
def cront():
    t      = time.time()
    t      = time.localtime(int(t))
    t      = time.strftime("%Y%m%d%H", t)
    key    = 'area_%s_*' % t
    key    = 'area_2018112812_*'
    z      = cache.gets(key)
    print(z)
    k      = 'area_%s' % t
    k      = 'area_2018112812'
    total  = 0
    d      = {}
    for a,b in z:
        prov = a.split('_')[2]
        num  = int(b)
        d[prov] = num
        total += num
    d['total'] = total
    d2s = json.dumps(d)
    cache.set(k, d2s)
    print(k)
    print(d2s)

cront()
