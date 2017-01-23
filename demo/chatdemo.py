#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import os
import uuid
import sys


from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

reload(sys)
sys.setdefaultencoding('utf8')

sys.path.insert(0, "../")
import aiml


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class MessageBuffer(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, cursor=None):
        # Construct a Future to return to our caller.  This allows
        # wait_for_messages to be yielded from a coroutine even though
        # it is not a coroutine itself.  We will set the result of the
        # Future when results are available.
        result_future = Future()
        if cursor:
            new_count = 0
            for msg in reversed(self.cache):
                if msg["id"] == cursor:
                    break
                new_count += 1
            if new_count:
                result_future.set_result(self.cache[-new_count:])
                return result_future
        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        # Set an empty result to unblock any coroutines waiting.
        future.set_result([])

    def new_messages(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for future in self.waiters:
            future.set_result(messages)
        self.waiters = set()
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]

    def clearcache(self):
        self.cache = []


# Making this a non-singleton is left as an exercise for the reader.
global_message_buffer = MessageBuffer()


class SigletonRobot(object):
    __instance = None
    Kernel = aiml.Kernel()
    Kernel.learn("load_aiml.xml")
    Kernel.respond("load aiml cnask")

    def __init__(self):
        pass

    def __new__(cls, *args, **kwd):
        if cls.__instance is None:
            cls.__instance = super(SigletonRobot, cls).__new__(cls, *args, **kwd)
        return cls.__instance


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=global_message_buffer.cache)


class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        conver = self.generate_conv(self, self.get_argument("body"))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            # self.write(conver[1])
            pass

        # enable log cach
        global_message_buffer.new_messages(conver)

    @staticmethod
    def generate_conv(self, inputstr):
        usermsg = {
            "id": str(uuid.uuid4()),
            "body": "User:" + inputstr,
        }
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        usermsg["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=usermsg))
        salebot = SigletonRobot()
        outputstr = salebot.Kernel.respond(inputstr)
        robotmsg = {
            "id": str(uuid.uuid4()),
            "body": "Robot:" + outputstr,
        }
        robotmsg["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=robotmsg))
        conver =  [usermsg, robotmsg]
        return conver


class MessageUpdatesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        cursor = self.get_argument("cursor", None)
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        self.future = global_message_buffer.wait_for_messages(cursor=cursor)
        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.future)


class MessageClearcachHandler(tornado.web.RequestHandler):
    def get(self):
        global_message_buffer.clearcache();


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/a/message/new", MessageNewHandler),
            (r"/a/message/updates", MessageUpdatesHandler),
            (r"/a/message/clearcach", MessageClearcachHandler)
            ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "boot_template"),
        static_path=os.path.join(os.path.dirname(__file__), "boot_static"),
        xsrf_cookies=False,
        debug=options.debug,
        )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
