# -*- coding: utf-8 -*-
# !/usr/bin/env python
from third_party import aiml


class AimlBrain(object):
    def __init__(self):
        self.kernel = aiml.Kernel()
        self.kernel.learn("load_aiml.xml")
        self.kernel.respond("load aiml cnask")

    def respond(self, inputstr):
        return self.kernel.respond(inputstr)

    def saveviable(self, vianame, viavalue):
        pass

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
