# -*- coding: utf-8 -*-
# !/usr/bin/env python
import pandas as pd


class Car(object):
    def __init__(self, attrlist, carid):
        self.result = pd.DataFrame()
        if carid is None:
            self.parad = {}
            for i in attrlist:
                self.parad[i] = ""
        else:
            self.carid = carid
            self.load_car(carid)

    def load_car(self, carno):
        pass

    def init_parad(self):
        for k in self.parad.keys():
            self.parad[k] = ""


if __name__ == "__main__":
    # for test
    pass
