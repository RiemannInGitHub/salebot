# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os
import sys

sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0] + "/..")
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

    def respond_with_viable(self, vialist, pattern):
        logger.debug("[respond_with_viable]the vialist:" + str(vialist))
        for i in vialist:
            pattern = pattern.replace("*", str(i), 1)
        logger.debug("[respond_with_viable]the inputstr:" + str(pattern))
        output = self.kernel.respond(pattern)
        logger.debug("[respond_with_viable]aiml respond:" + str(output))
        return output

    # -------------------------------------------------------------
    # function: send msg to aiml to talk with aiml
    # args: msg -- msg
    # return: output -- result
    # describe: aiml is an independent module, so by sendmsg to let it remember or answer sth
    # -------------------------------------------------------------
    def save_viable(self, vianame, viavalue):
        logger.debug("aiml save via:" + vianame + "," + viavalue)
        message = "{SAVE:{" + vianame + ':' + viavalue + "}}"
        logger.debug("aiml save return:" + self.respond(message))


if __name__ == "__main__":
    # for test
    aiml = AimlBrain()
    while(1):
        print(aiml.respond(raw_input(">")))
