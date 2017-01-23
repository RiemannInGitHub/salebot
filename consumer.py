# -*- coding: utf-8 -*-
# !/usr/bin/env python


class Consumer(object):
    def __init__(self):
        self.username = ""
        self.userkey = ""
        self.Car = ""
        self.Carlist = []

    def loaduser(self, userkey):
        self.userkey = userkey

    def currentcar(self, currentcar):
        self.Car = currentcar
        self.Carlist.append(currentcar)

if __name__ == "__main__":
    # for test
    pass
