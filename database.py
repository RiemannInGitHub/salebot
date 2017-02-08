#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import json
from util import log
from macro import *

logger = log.get_logger(__name__)

testdb = '[\
        {"CARBRAND":"长安", "CARNAME":"CS15", "CARMODEL":"2016款 1.5L 手动舒适版","PRICE":"5.79万", "TYPE":"小型SUV", "SEATS":"5座", "ENGINE":"1.5L 107马力 L4", "GEARBOX":"5挡手动", "OILCONSUMPTION":"6.3L/100km", "ROZ":"93号(京92号)"},\
        {"CARBRAND":"长安", "CARNAME":"CS15", "CARMODEL":"2016款 1.5L 手动时尚版","PRICE":"6.39万", "TYPE":"小型SUV", "SEATS":"5座", "ENGINE":"1.5L 107马力 L4", "GEARBOX":"5挡手动", "OILCONSUMPTION":"6.3L/100km", "ROZ":"93号(京92号)"},\
        {"CARBRAND":"长安", "CARNAME":"CS15", "CARMODEL":"2016款 1.5L 手动豪华版","PRICE":"6.89万", "TYPE":"小型SUV", "SEATS":"5座", "ENGINE":"1.5L 107马力 L4", "GEARBOX":"5挡手动", "OILCONSUMPTION":"6.3L/100km", "ROZ":"93号(京92号)"},\
        {"CARBRAND":"丰田", "CARNAME":"汉兰达", "CARMODEL":"2015款 2.0T 两驱精英版 5座","PRICE":"23.98万", "TYPE":"中型SUV", "SEATS":"5座", "ENGINE":"2.0T 220马力 L4", "GEARBOX":"6挡手自一体", "OILCONSUMPTION":"8.2L/100km", "ROZ":"97号(京95号)"},\
        {"CARBRAND":"丰田", "CARNAME":"汉兰达", "CARMODEL":"2015款 2.0T 两驱精英版 7座","PRICE":"24.88万", "TYPE":"中型SUV", "SEATS":"7座", "ENGINE":"2.0T 220马力 L4", "GEARBOX":"6挡手自一体", "OILCONSUMPTION":"8.2L/100km", "ROZ":"97号(京95号)"},\
        {"CARBRAND":"丰田", "CARNAME":"汉兰达", "CARMODEL":"2015款 2.0T 四驱精英版 7座","PRICE":"25.88万", "TYPE":"中型SUV", "SEATS":"7座", "ENGINE":"2.0T 220马力 L4", "GEARBOX":"6挡手自一体", "OILCONSUMPTION":"8.2L/100km", "ROZ":"97号(京95号)"}\
         ]'


class Database(object):
    # link db which contain car's data
    def __init__(self):
        self.result = pd.DataFrame()

    @staticmethod
    def generate_attrdict():
        df = pd.read_json(testdb)
        dfdict = df.to_dict()
        return dfdict

    # flag-true query from result, flag-false query from cardb
    # TODO: if api return db less than 100, get all of it; else keep ask user add more condition
    def query_by_condition(self, condition, flag):
        if flag:
            self.result = self.fliter_dataframe(condition, self.result)
        else:
            self.result = self.fliter_dataframe(condition, pd.read_json(testdb))

    def query_result(self, condition):
        pass

    @staticmethod
    def fliter_dataframe(condition, df):
        for k, v in condition.iteritems():
            if v != "":
                df = df.loc[df[k] == v]
        return df

    def get_label_value(self, label):
        result = []
        valuel = self.result[label].values
        for i in valuel:
            if i not in result:
                result.append(i)
        return len(result), result

if __name__ == "__main__":
    # for test
    database = Database()
    conditiond = {CARBRAND: u"长安", CARNAME: u"CS15", CARMODEL: u"", PRICE: u"", TYPE: u"", SEATS: u"",
                    ENGINE: u"", GEARBOX: u"", OILCONSUMPTION: u"", ROZ: u""}
    database.query_by_condition(conditiond, False)
    lenth, value = database.get_label_value(PRICE)
    database.generate_attrdict()
    logger.warning("success")
