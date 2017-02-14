#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import re
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
    def __init__(self):
        self.result = pd.DataFrame()

    @staticmethod
    def generate_attrlist():
        df = pd.read_json(testdb)
        return df.columns.values

    @staticmethod
    def price_fliter(column, condition, df):
        indexl = []
        paral = condition.splite("-")
        for valuestr in df[column].values:
            valuei = int(re.search('/d+', valuestr))
            if paral[0] <= valuei <= paral[1]:
                indexl.append(df[column].values.index(df[column].values))
        return df.loc[indexl, :]

    @staticmethod
    def contain_filter(column, condition, df):
        indexl = []
        for valuestr in df[column].values:
            if valuestr.find(condition):
                indexl.append(df[column].values.index(df[column].values))
        return df.loc[indexl, :]

    # flag-true query from result, flag-false query from cardb & refresh result
    # TODO: if api return db less than 100, get all of it; else keep ask user add more condition
    def query_by_condition(self, condition, flag):
        logger.debug("database query flag is " + str(flag) + " :(true)from db,(false)from result")
        if flag:
            self.result = self.fliter_dataframe(condition, pd.read_json(testdb))
        else:
            self.result = self.fliter_dataframe(condition, self.result)

    def fliter_dataframe(self, condition, df):
        for k, v in condition.iteritems():
            if v != "":
                if k == PRICE:
                    df = self.price_fliter(k, v, df)
                else:
                    df = self.contain_filter(k, v, df)
        logger.debug("fliter condition is:" + str(condition))
        logger.debug("database result change to:\n" + str(df))
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
    lenth, value = database.get_label_value(PRICE)
    logger.warning("success")
