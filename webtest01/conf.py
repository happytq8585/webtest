#-*- coding: utf-8 -*-
import ConfigParser

class ServerConf():
    def __init__(self, name):
        p = ConfigParser.ConfigParser()
        p.read(name)
        self.ip         = p.get('sys', 'ip')
        self.port       = p.getint('sys', 'port')
        self.ip_parser  = p.get('sys', 'ip_parser')

        self.redis_ip   = p.get('redis', 'redis_ip')
        self.redis_port = p.getint('redis', 'redis_port')
        self.redis_db   = p.getint('redis', 'redis_db')
        self.redis_password = p.get('redis', 'redis_password')
        self.redis_timeout = p.getint('redis', 'redis_timeout')

    def dis(self):
        print(self.ip)
        print(self.port)
        print(self.ip_parser)
        print(self.redis_ip)
        print(self.redis_port)
        print(self.redis_db)
        print(self.redis_password)
        print(self.redis_timeout)

conf    = ServerConf('./conf.txt')

if __name__ == "__main__":
    conf.dis()
