# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import json
import sys
import re
from macro import *
from util import log
from util import tool
from fuzzywuzzy import fuzz

reload(sys)
sys.setdefaultencoding('utf8')

logger = log.get_logger(__name__)


class Analyze(object):
    def __init__(self):
        self.patterndf = pd.read_csv("corpus/pattern.csv")
        self.querydf = pd.read_csv("corpus/querydict.csv")
        self.searchdf = pd.read_csv("corpus/searchdict.csv")
        self.gen_funclist = {
            None: self.pattern_none,
            "WELCOME": self.pattern_welcome,
            "QUERY": self.pattern_query,
            "SEARCH": self.pattern_search,
            "FUZZYQUERY": self.pattern_fuzzyquery,
            "SEARCHQUERY": self.pattern_searchquery,
            "COMPARE": self.pattern_compare
        }
        self.price = ""
        self.price_pattern = {re.compile(u'\d+万到\d+万'): "between",
                              re.compile(u'\d+万'): "equal",
                              re.compile(u'大于\d+万'): "greater",
                              re.compile(u'小于\d+万'): "less",
                              re.compile(u'\d+万左右'): "around",
                              re.compile(u'\d{2}十万'): "between10",
                              re.compile(u'\d{2}十万左右'): "between10"}

    def price_process(self, wordstr):
        value = wordstr
        index = 0
        v = ""
        for m, v in self.price_pattern:
            if m.match(wordstr):
                break
            index += 1
        if v == "equal":
            numl = re.findall('/d+', wordstr)
            minn = int(numl[0]) - 5
            maxn = int(numl[0]) + 5
            value = str(maxn) + '-' + str(minn)
        elif v == "between":
            numl = re.findall('/d+', wordstr)
            numl.sort()
            minn = int(numl[0]) - 5
            maxn = int(numl[1]) + 5
            value = str(maxn) + '-' + str(minn)
        elif v == "greater":
            numl = re.findall('/d+', wordstr)
            value = numl[0] + '-' + str(UTIMAXPRICE)
        elif v == "less":
            numl = re.findall('/d+', wordstr)
            value = str(0) + "-" + numl[0]
        elif v == "around":
            numl = re.findall('/d+', wordstr)
            basenum = int(numl[0])
            value = str(basenum - 5) + '-' + str(basenum + 5)
        elif v == "between10":
            numl = re.findall('/d', wordstr)
            minn = int(numl[0]) * 10 - 5
            maxn = int(numl[1]) * 10 + 5
            value = str(maxn) + '-' + str(minn)
        return value

    def classify_word(self, word, strlist):
        strindex = strlist.index(word)
        result, index, wordstr = tool.df_inlude_search(self.searchdf, strlist[strindex:], "value", False)
        if result is False:
            return result
        label = self.searchdf["label"][index]
        if label is PRICE:
            value = self.price_process(wordstr)
        else:
            value = wordstr
        return result, label, value, wordstr

    # TODO:for price and model the include problem not solved, need to write a func for it
    def set_label(self, inputstr):
        labelrinput = inputstr
        labelinput = inputstr
        result = tool.cut_no_blank(inputstr)
        for word in result:
            result, label, value, originstr = self.classify_word(word, result)
            if result:
                labelrinput = labelrinput.replace(originstr, value, 1)
                labelinput = labelinput.replace(originstr, label + " " + value + " ", 1)
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

    def pattern_welcome(self, inputstr):
        return "WELCOME"

    def pattern_query(self, labelinput):
        inputl = tool.cut_no_blank(labelinput)
        output = "QUERY "
        outputl = []
        for word in inputl:
            strindex = inputl.index(word)
            result, index = tool.df_inlude_search(self.querydf, inputl[strindex:], "value", False)
            logger.debug("[QUERY]pattern_query word is " + word + "inlude_search result is " + str(result))
            if result:
                outputl = tool.insert_list_norepeat(outputl, self.querydf["label"][index])
        output += json.dumps(outputl)
        return output

    def pattern_search(self, labelinput):
        inputl = tool.cut(labelinput)
        output = "SEARCH "
        outputd = {}
        index = 0
        for word in inputl:
            if word in self.searchdf["label"].values:
                outputd[word] = "".join(inputl[index+2: inputl[index + 1:].index(" ")])
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
        logger.info("pattern: " + unicode(pattern))

        try:
            output = self.gen_output(pattern, labelinput)
        except Exception as e:
            logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
            log.log_traceback()
            return

        logger.info("normalize to aiml: " + str(output))
        return output

if __name__ == "__main__":
    # for test
    analyze = Analyze({})

