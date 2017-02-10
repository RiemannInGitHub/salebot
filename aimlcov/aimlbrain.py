# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os
from third_party import aiml
from util import log

logger = log.get_logger(__name__)


class AimlBrain(object):
    def __init__(self, aimlpath=os.path.split(os.path.realpath(__file__))[0] + "/load_aiml.xml"):
        print(aimlpath)
        self.kernel = aiml.Kernel()
        self.kernel.learn(aimlpath)
        self.kernel.respond("load aiml start")

    def respond(self, inputstr):
        return self.kernel.respond(inputstr)

    def respond_with_viable(self, vialist, inputstr):
        for i in vialist:
            inputstr.replace('*', i, 1)
        return self.kernel.respond(inputstr)

    # TODO: use json create msg or write a func for it
    def save_viable(self, vianame, viavalue):
        message = "{SAVE:{" + vianame + ':' + viavalue + "}}"
        logger.debug("aiml save return:" + self.respond(message))
        print(self.respond(message))

    # -------------------------------------------------------------
    # function: send msg to aiml to talk with aiml
    # args: msg -- msg
    # return: output -- result
    # describe: aiml is an independent module, so by sendmsg to let it remember or answer sth
    # -------------------------------------------------------------
    def send_msg(self, msg):
        return self.kernel.respond(msg)

if __name__ == "__main__":
    # for test
    aiml = AimlBrain()
    while(1):
        print(aiml.respond(raw_input(">")))
