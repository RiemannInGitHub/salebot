# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os
from macro import *
from third_party import aiml


class AimlBrain(object):
    def __init__(self, aimlpath=os.path.split(os.path.realpath(__file__))[0] + "/load_aiml.xml"):
        print(aimlpath)
        self.kernel = aiml.Kernel()
        self.kernel.learn(aimlpath)
        self.kernel.respond("load aiml start")

    def respond(self, inputstr):
        return self.kernel.respond(inputstr)

    def saveviable(self, vianame, viavalue):
        assert(vianame in AIMLVAR)
        message = '{SAVE:' + vianame + ' is ' + viavalue
        print(self.respond(message))

    # -------------------------------------------------------------
    # function: send msg to aiml to talk with aiml
    # args: msg -- msg
    # return: output -- result
    # describe: aiml is an independent module, so by sendmsg to let it remember or answer sth
    # -------------------------------------------------------------
    def sendmsg(self, msg):
        return self.kernel.respond(msg)

if __name__ == "__main__":
    # for test
    aiml = AimlBrain()
    while(1):
        print(aiml.respond(raw_input(">")))
