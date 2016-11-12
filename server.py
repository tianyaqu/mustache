#!/usr/bin/env python
# coding=utf-8

import re
import os.path
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

from handler.home import HomeHandler
from handler.wshandler import Detector

define("port",default=443,help="run on a given port",type=int)

class Mustache(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",HomeHandler),
            (r"/detector",Detector),
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            debug = True,
            cookie_secret = 'Secretcookie',
        )

        tornado.web.Application.__init__(self,handlers,**settings)

def run():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Mustache(),ssl_options={
    "certfile": os.path.join(os.path.abspath("cert/"), "chained.pem"),
    "keyfile": os.path.join(os.path.abspath("cert/"), "domain.key"),
    })
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    run()
