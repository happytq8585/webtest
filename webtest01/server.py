#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import json
import time
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler
from tornado.options import define, options

from conf import conf
from cache import cache

define("port", default=conf.port, help="run on the given port", type=int)

def current_time():
    t  = time.time()
    t1 = int(t+300)/300*300
    t1 = time.localtime(t1)
    r1 = time.strftime("%Y%m%d%H%M", t1)
    t2 = int(t+3600)/3600*3600
    t2 = time.localtime(t2)
    r2 = time.strftime("%Y%m%d%H", t2)
    return r1,r2

def cront():
    t      = time.time()
    if int(t) % 3600 != 0:
        return
    t      = time.localtime(int(t))
    t      = time.strftime("%Y%m%d%H", t)
    key    = 'area_%s_*' % t
    z      = cache.gets(key)
    k      = 'area_%s' % t
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

class IndexHandler(RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        ip = self.request.headers.get("X-Real-Ip", "")
        ip = self.request.remote_ip if not ip else ip
        t1,t2  = current_time()
        key = 'get_%s' % t1
        r = cache.incr(key)
        msg = 'You are the %d time(s) access time=%s region=' % (r, t1)

        url = conf.ip_parser % ip
        http_client = tornado.httpclient.AsyncHTTPClient()
        res = yield tornado.gen.Task(http_client.fetch, url)
        try:
            body = json.loads(res.body)
            if not body.get('data', None):
                body['data'] = {}
        except:
            body = {'data':{}}
        region = body['data'].get('region', 'unknown')
        key = 'area_%s_%s' % (t2, region)
        cache.incr(key)
        self.write(msg)
        self.write(region)
        self.finish()

    def post(self):
        ip = self.request.headers.get("X-Real-Ip", "")
        ip = self.request.remote_ip if not ip else ip
        t1, t2  = current_time()
        key = 'post_%s' % t1
        r = cache.incr(key)
        msg = 'You are the %d time(s) access' % r

        url = conf.ip_parser % ip
        http_client = tornado.httpclient.AsyncHTTPClient()
        res = yield tornado.gen.Task(http_client.fetch, url)
        try:
            body = json.loads(res.body)
            if not body.get('data', None):
                body['data'] = {}
        except:
            body = {'data':{}}
        region = body['data'].get('region', 'unknown')
        key = 'area_%s_%s' % (t2, region)
        cache.incr(key)
        self.write(msg)
        self.write(region)
        self.finish()

class QueryGetPostHandler(RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        t = self.get_argument('time', None)
        k = self.get_argument('kind', None)
        if not t or not k:
            msg = 'invalid parameter! time=&kind=&'
            self.write(msg)
        else:
            key = '%s_%s' % (k, t)
            val = cache.get(key)
            val = 0 if not val else int(val)
            msg = 'number is %d' % val
            self.write(msg)
        self.finish()



class QueryAreaHandler(RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        t = self.get_argument('time', None)
        if not t:
            t0, t = current_time()
        key = 'area_%s' % t
        val = cache.get(key)
        val = val if val else 'None'
        val = val.decode('unicode_escape')
        self.write(val)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": False,
        "debug":False}
    handler = [
        (r"/static/(.*)", StaticFileHandler, {"path": "static"}),  
        (r"/css/(.*)", StaticFileHandler, {"path": "static/css"}),  
        (r"/js/(.*)", StaticFileHandler, {"path": "static/js"}),  
        (r"/img/(.*)", StaticFileHandler, {"path": "static/img"}), 
        ('/webtest', IndexHandler),
        ('/query_getpost', QueryGetPostHandler),
        ('/query_area', QueryAreaHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.PeriodicCallback(cront, 1000).start()
    tornado.ioloop.IOLoop.instance().start()
