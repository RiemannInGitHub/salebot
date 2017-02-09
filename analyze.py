# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from macro import *
from util import log
from util import tool
from fuzzywuzzy import fuzz


logger = log.get_logger(__name__)


class Analyze(object):
    def __init__(self, labeldict):
        self.labeldict = labeldict
        self.patterndf = pd.read_csv("corpus/pattern.csv")
        self.normalizedf = pd.read_csv("corpus/normalize.csv")
        self.gen_funclist = {
            "WELCOME": self.pattern_welcome,
            "QUERY": self.pattern_query,
            "SEARCH": self.pattern_search,
            "FUZZYQUERY": self.pattern_fuzzyquery,
            "SEARCHQUERY": self.pattern_searchquery,
            "COMPARE": self.pattern_compare
        }
        self.special_key = {
            PRICE: self.special_price,
            CARMODEL: self.special_carmodel,
        }

    # -------------------------------------------------------------
    # function: set labels in an input
    # args: input -- inputstr eg: "长安c15"
    # return: output -- input with labels eg: "carbrand长安<carmodel>c15"
    # -------------------------------------------------------------
    # TODO:for price and model the include problem not solved, need to write a func for it
    def set_label(self, inputstr):
        labelrinput = inputstr
        labelinput = ""
        result = tool.cut_no_blank(inputstr)
        for word in result:
            label = [k for k, v in self.labeldict.iteritems() if word in v.values()]
            if len(label) != 0:
                labelinput = labelinput + ' ' + label.pop() + ' '
                labelrinput.replace(word, label, 1)
            labelinput = labelinput + word
        return labelinput, labelrinput

    def search(self, labelrinput):
        score = {"score": 0, "index": 0}
        index = 0
        for question in self.patterndf["question"].values:
            tmpscore = fuzz.ratio(question, str(labelrinput))
            if tmpscore > score["score"]:
                score["score"] = tmpscore
                score["index"] = index
            index += 1

        logger.debug("labelrinput max score is " + str(score["score"]))

        if score["score"] > 50:
            return self.patterndf["category"][score["index"]]
        else:
            return None

    def pattern_welcome(self):
        return "WELCOME"

    # TODO:muliti query need to be added
    def pattern_query(self, labelinput):
        inputl = tool.cut_no_blank(labelinput)
        output = "QUERY"
        for word in inputl:
            result, index, column = tool.df_inlude_search(self.normalizedf, word, "value")
            if result:
                output += ' ' + self.normalizedf["label"][index] + ' '
        return output

    def special_price(self, inputstring):
        pass

    def special_carmodel(self, inputstring):
        pass

    def pattern_search(self, labelinput):
        inputl = tool.cut_no_blank(labelinput)
        output = "SEARCH"
        index = 0
        for word in inputl:
            if word in self.special_key.keys():
                s, inputl = self.special_key[word](inputl)
                output += ' ' + str(s) + ' '
            else:
                # TODO: fuzzy match should be consider&design, now is too specific
                s = word + ' ' + inputl[index + 1]
                output += ' ' + s + ' '
            index += 1
        return output

    def pattern_fuzzyquery(self, labelinput):
        pass

    def pattern_searchquery(self, labelinput):
        pass

    def pattern_compare(self, labelinput):
        pass

    def gen_output(self, pattern, labelinput):
        gen_func = self.gen_funclist[pattern]
        return gen_func(labelinput)

    # -------------------------------------------------------------
    # function: normalize inputstr
    # args: input -- inputstr
    # return: output -- normalized input
    # -------------------------------------------------------------
    def normalize(self, inputstr):
        logger.info("input:" + inputstr)

        labelinput, labelrinput = self.set_label(inputstr)
        logger.debug("input with label:" + labelinput)
        logger.debug("input with label replaced:" + labelrinput)

        pattern = self.search(labelrinput)
        logger.debug("pattern:" + str(pattern))

        output = self.gen_output(pattern, labelinput)
        logger.info("output:" + output)
        return output

if __name__ == "__main__":
    # for test
    analyze = Analyze({})

