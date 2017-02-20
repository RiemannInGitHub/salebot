# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_config_file


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class MessageWordbotHandler(tornado.web.RequestHandler):
    pass

class MessageAudiobotHandler(tornado.web.RequestHandler):
    pass

class Api(object):
    def __init__(self):
        parse_config_file("server.conf")
        self.debug = options.debug
        self.port = options.api_port
        self.app = tornado.web.Application(
            [
                (r"/", MainHandler),
                (r"/wordbot", MessageWordbotHandler),
                (r"/audiobot", MessageAudiobotHandler),
            ],
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "demo/api_template"),
            static_path=os.path.join(os.path.dirname(__file__), "demo/api_static"),
            xsrf_cookies=False,
            debug=self.debug,
        )

    def listen(self):
        self.app.listen(self.port)

if __name__ == "__main__":
    # for test
    api = Api()
    api.listen()
    tornado.ioloop.IOLoop.current().start()

