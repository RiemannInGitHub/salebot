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

if __name__ == "__main__":
    # for test
    aiml = AimlBrain()
    while(1):
        print(aiml.respond(raw_input(">")))
