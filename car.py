# -*- coding: utf-8 -*-
# !/usr/bin/env python
from macro import *


class Car(object):
    def __init__(self, attrlist):
        self.prize = 0
        self.parad = {}
        for i in attrlist:
            self.parad[i] = ""

    def load_car(self, carno):
        pass


if __name__ == "__main__":
    # for test
    pass
