# -*- coding: utf-8 -*-
# !/usr/bin/env python
import aimlcov
import analyze
import consumer
import car
import os
import json
import re
from macro import *


class SaleBot(object):
    def __init__(self, userkey=None, currentcar=None,
                 aimlpath=os.path.split(os.path.realpath(__file__))[0] + "/aimlcov/load_aiml.xml"):
        self.__aiml = aimlcov.AimlBrain(aimlpath)
        self.consumer = consumer.Consumer()
        self.car = car.Car()
        if userkey:
            self.get_user_by_key(userkey)

        self.msgregex = re.compile('\{.+\}')
        self.msgfunclist = {
            'SET':      self.msg_set_handle,
            'QUERY':    self.msg_query_handle,
        }
        self.msgdict = {
            'carbrand': self.car.set_brand,
            'carmodel': self.car.set_model,
        }

    def get_user_by_key(self, userkey):
        self.consumer.load_user(userkey)
        # self.aiml.save_viable(USERKEY, userkey)

    def msg_set_handle(self, msg):
        for k, v in msg.items():
            handler = self.msgdict[k]
            handler(v)

    def msg_query_handle(self, msg):
        pass

    # -------------------------------------------------------------
    # function: receive msg from aiml to remember sth
    # args: response -- response
    # return:
    # describe: aiml is an independent module, so by sendmsg to remember sth from it
    # -------------------------------------------------------------
    def respond_analyze(self, response):
        m = self.msgregex.match(response)
        output = ""

        if m is not None:
            text = response[m.end():]
            string = m.group()
            msg = json.loads(string)
            for msgtype in msg.keys():
                handlefunc = self.msgfunclist[msgtype]
                output = handlefunc(msg[msgtype])
                if output is None:
                    output = text
        else:
            output = response

        return output

    # -------------------------------------------------------------
    # function: construct output for user's input
    # args: input -- input
    # return: output -- input
    # describe: there are few steps for progressing
    #           1) normalize input or transform input to robot recognise pattern
    #           2) find direct answer from knowledge (no use temp)
    #           3) aiml progressing
    #           4) analyze aiml respond for robot thinking
    # -------------------------------------------------------------
    def respond(self, inputstr):

        labalinput = analyze.set_label(inputstr)
        normalinput = analyze.normalize(labalinput)
        output = self.respond_analyze(self.__aiml.respond(normalinput))

        return output

if __name__ == "__main__":
    # for test
    salerobot = SaleBot()
    while(1):
        print(salerobot.respond(raw_input(">")))


