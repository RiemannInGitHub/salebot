# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import json
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
            None: self.pattern_none,
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
                labelrinput = labelrinput.replace(word, label[0], 1)
                labelinput = labelinput + ' ' + label[0] + ' '
            labelinput = labelinput + word
        return labelinput, labelrinput

    def search(self, labelrinput):
        score = {"score": 0, "index": 0}
        index = 0
        for question in self.patterndf["question"].values:
            _, labelrquestion = self.set_label(question)
            tmpscore = fuzz.ratio(labelrquestion, labelrinput)
            if tmpscore > score["score"]:
                score["score"] = tmpscore
                score["index"] = index
            # TODO：improve log.py support showing specific log
            # logger.debug("labelrquestion is " + str(labelrquestion))
            # logger.debug("tmpscore is " + str(tmpscore))
            index += 1
        logger.debug("labelrinput max score is " + unicode(score["score"]))

        if score["score"] > 50:
            return self.patterndf["category"][score["index"]]
        else:
            return None

    def pattern_none(self, inputstr):
        return inputstr

    def pattern_welcome(self, input):
        return "WELCOME"

    # TODO:muliti query need to be added
    def pattern_query(self, labelinput):
        inputl = tool.cut_no_blank(labelinput)
        output = "QUERY"
        for word in inputl:
            result, index, column = tool.df_inlude_search(self.normalizedf, word, "value")
            if result:
                output += ':' + self.normalizedf["label"][index]
        return output

    def special_price(self, inputstring):
        pass

    def special_carmodel(self, inputstring):
        pass

    # TODO:muliti search need to be added
    # TODO:use json replace the data trans
    def pattern_search(self, labelinput):
        inputl = tool.cut_no_blank(labelinput)
        output = "SEARCH "
        outputd = {}
        index = 0

        for word in inputl:
            if word in self.special_key.keys():
                s, inputl = self.special_key[word](inputl)
                outputd[word] = unicode(s)
            elif word in self.labeldict.keys():
                # TODO: fuzzy match should be consider&design, now is too specific
                outputd[word] = inputl[index + 1]
            index += 1

        output += json.dumps(outputd)
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
        logger.info("input: " + inputstr)

        try:
            labelinput, labelrinput = self.set_label(inputstr)
        except Exception as e:
            logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
            log.log_traceback()
            return
        logger.info("input with label: " + labelinput)
        logger.info("input replaced label: " + labelrinput)

        try:
            pattern = self.search(labelrinput)
        except Exception as e:
            logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
            log.log_traceback()
            return
        logger.debug("pattern: " + unicode(pattern))

        try:
            output = self.gen_output(pattern, labelinput)
        except Exception as e:
            logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
            log.log_traceback()
            return

        logger.debug("normalize to aiml: " + output)
        return output

if __name__ == "__main__":
    # for test
    analyze = Analyze({})

