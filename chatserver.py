#!/usr/bin/env python

import logging
import os
import sys
import uuid

import tornado.escape
import tornado.ioloop
import tornado.web
import wordbot.manager as manager
from tornado import gen
from tornado.concurrent import Future
from tornado.options import define, options, parse_command_line

reload(sys)
sys.setdefaultencoding('utf8')




define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

def get_user_ip(ip):
    if ip == "::1":
        ip = "localhost"
    return ip

class MessageBuffer(object):
    def __init__(self):
        self.waiters = {}
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, cursor=None, user=None):
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
        self.waiters[user] = result_future
        return result_future

    def cancel_wait(self, future):
        for key in self.waiters.keys():
            if self.waiters[key] == future:
                del self.waiters[key]
        # Set an empty result to unblock any coroutines waiting.
        future.set_result([])

    def new_messages(self, messages, user):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for key in self.waiters.keys():
            if key == user:
                future = self.waiters[key]
                future.set_result(messages)
        # self.waiters = set()
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]

    def clear_cache(self, user):
        for index in range(len(self.cache)-1, -1, -1):
            if user == self.cache[index]['username']:
                self.cache.remove(self.cache[index])

# Making this a non-singleton is left as an exercise for the reader.
global_message_buffer = MessageBuffer()
global_manager = manager.Manager()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        username = get_user_ip(self.request.remote_ip)
        self.render("index.html", messages=self.generate_cache(username))

    def generate_cache(self, username):
        result = []
        for message in global_message_buffer.cache:
            if username == message['username']:
                result.append(message)
        return result



class MessageNewHandler(tornado.web.RequestHandler):

    def post(self):
        self.username = get_user_ip(self.request.remote_ip)
        logging.info("MessageNewHandler username is " + str(self.username))
        conver = self.generate_conv(self.get_argument("body"))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            # self.write(conver[1])
            pass

        # enable log cache
        global_message_buffer.new_messages(conver, self.username)

    def generate_conv(self, inputstr):
        usermsg = {
            "id": str(uuid.uuid4()),
            "body": "User(" + self.username + "):" + inputstr,
            "username": self.username,
        }
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        usermsg["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=usermsg))

        salebot = global_manager.get_create_bot(self.username)
        outputstr = salebot.respond(inputstr)

        robotmsg = {
            "id": str(uuid.uuid4()),
            "body": "Robot:" + outputstr,
            "username": self.username,
        }
        robotmsg["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=robotmsg))
        conver = [usermsg, robotmsg]
        return conver


class MessageUpdatesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        self.username = get_user_ip(self.request.remote_ip)
        cursor = self.get_argument("cursor", None)
        logging.info("MessageUpdatesHandler cursor is " + str(cursor))
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        global_manager.get_create_bot(self.username)
        self.future = global_message_buffer.wait_for_messages(cursor=cursor, user=self.username)
        messages = yield self.future
        if self.request.connection.stream.closed():
            # TODO: need to consider how to del bo use bot
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.future)


class MessageClearcachHandler(tornado.web.RequestHandler):
    def get(self):
        username = get_user_ip(self.request.remote_ip)
        global_message_buffer.clear_cache(username)


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
        template_path=os.path.join(os.path.dirname(__file__), "wordbot/demo/boot_template"),
        static_path=os.path.join(os.path.dirname(__file__), "wordbot/demo/boot_static"),
        xsrf_cookies=False,
        debug=options.debug,
        )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
