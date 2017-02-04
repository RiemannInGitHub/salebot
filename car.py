# -*- coding: utf-8 -*-
# !/usr/bin/env python


class Car(object):
    def __init__(self):
        self.prize = 0
        self.brand = ""
        self.model = ""

    def loadcar(self, carno):
        pass

    def setbrand(self, value):
        self.brand = value

    def setmodel(self, value):
        self.model = value

if __name__ == "__main__":
    # for test
    pass
