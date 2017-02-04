# -*- coding: utf-8 -*-
# !/usr/bin/env python
import car


class Consumer(object):
    def __init__(self):
        self.username = ""
        self.userkey = ""
        self.carlist = []

    def loaduser(self, userkey):
        self.userkey = userkey

if __name__ == "__main__":
    # for test
    pass
