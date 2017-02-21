# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import wordbot.manager as manager

import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_config_file


# temp usr info

USERINFO = {"wangye": "51b500fa-2662-4a24-9180-2650ae8ad41b",
            "SAAS": "0801a8bf-97c6-4fad-91e8-8e25e2bf7dba"}

# ERRCODE
MSG_OK = 10000
MSG_ERR = 20000
MSG_USR_NO_EXIST = 20010
MSG_APPKEY_ERR = 20020
MSG_WORDBOT_ERR = 20030
MSG_AUDIOPRO_ERR = 20040
MSG_INPUT_PARA_ERR = 20050
RETDICT = {MSG_OK:u"成功",
           MSG_ERR: u"成功",
           MSG_USR_NO_EXIST: u"用户不存在",
           MSG_APPKEY_ERR: u"Appkey验证失败",
           MSG_WORDBOT_ERR: u"文字处理引擎异常",
           MSG_AUDIOPRO_ERR: u"语音转换异常",
           MSG_INPUT_PARA_ERR: u"请输入正确的用户名和AppKey"}

api_global_manager = manager.Manager()

def user_identify(userid, appkey):
    if userid == "" or appkey == "":
        return MSG_INPUT_PARA_ERR
    if userid not in USERINFO.keys():
        return MSG_USR_NO_EXIST
    if USERINFO[userid] != appkey:
        return MSG_APPKEY_ERR
    return MSG_OK


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


# TODO: default is json, in the future can suport xml&json option
class MessageWordbotHandler(tornado.web.RequestHandler):

    def post(self):
        body = ""
        userid = self.get_argument("userid")
        appkey = self.get_argument("appkey")
        inputstr = self.get_argument("inputtext")
        retcode = user_identify(userid, appkey)
        if retcode == MSG_OK:
            salebot = api_global_manager.get_create_bot(userid)
            body = salebot.respond(inputstr)
        self.output(retcode, body)

    def output(self, retcode, body):
        desc = RETDICT[retcode]
        redict = {"retcode": retcode,
                  "describe": desc,
                  "body": body}
        rejson = json.dumps(redict)
        self.write(rejson)


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
            static_path=os.path.join(os.path.dirname(__file__), "demo/api_template"),
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

