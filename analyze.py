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
        self.patterndf = pd.read_csv("corpus/pattern.csv", encoding="utf_8")
        self.querydf = pd.read_csv("corpus/querydict.csv", encoding="utf_8")
        self.searchdf = pd.read_csv("corpus/searchdict.csv", encoding="utf_8")
        self.gen_funclist = {
            "WELCOME": self.pattern_welcome,
            "QUERY": self.pattern_query,
            "SEARCH": self.pattern_search,
            "FUZZYQUERY": self.pattern_fuzzyquery,
            "SEARCHQUERY": self.pattern_searchquery,
            "COMPARE": self.pattern_compare,
            "PARA": self.pattern_para,
        }
        self.price = ""
        self.price_pattern = {re.compile(u'\d+万到\d+万'): "between",
                              re.compile(u'\d+万'): "equal",
                              re.compile(u'大于\d+万'): "greater",
                              re.compile(u'小于\d+万'): "less",
                              re.compile(u'\d+万左右'): "around",
                              re.compile(u'\d{2}十万'): "between10",
                              re.compile(u'\d{2}十万左右'): "between10"}
        self._label_para = {"label": "",
                            "value": "",
                            "wordstr": "",
                            "endindex": 0}

        for index, row in self.patterndf.iterrows():
            _, row["question"] = self.set_label(row["question"])

    def price_process(self, wordstr):
        wordstr = tool.num_process(wordstr)
        value = wordstr
        v = ""
        num_re = re.compile(u'\d+')
        num_one_re = re.compile(u'\d')
        for m, v in self.price_pattern.iteritems():
            if m.match(wordstr):
                break
        if v == "equal":
            numl = num_re.findall(wordstr)
            minn = int(numl[0]) - 5
            maxn = int(numl[0]) + 5
            value = str(minn) + '-' + str(maxn)
        elif v == "between":
            numl = num_re.findall(wordstr)
            numl.sort()
            minn = int(numl[0]) - 5
            maxn = int(numl[1]) + 5
            value = str(minn) + '-' + str(maxn)
        elif v == "greater":
            numl = num_re.findall(wordstr)
            value = numl[0] + '-' + str(UTIMAXPRICE)
        elif v == "less":
            numl = num_re.findall(wordstr)
            value = str(0) + "-" + numl[0]
        elif v == "around":
            numl = num_re.findall(wordstr)
            basenum = int(numl[0])
            value = str(basenum - 5) + '-' + str(basenum + 5)
        elif v == "between10":
            numl = num_one_re.findall(wordstr)
            minn = int(numl[0]) * 10 - 5
            maxn = int(numl[1]) * 10 + 5
            value = str(minn) + '-' + str(maxn)
        return value

    def classify_word(self, word, strlist):
        result, index, wordstr, endindex = tool.df_inlude_search(self.searchdf, strlist, "value", False)

        if not result:
            # logger.debug("[SETLABEL]False:(word)" + word)
            return result
        label = self.searchdf["label"][index]
        if label == PRICE:
            value = self.price_process(wordstr)
        else:
            value = wordstr

        self._label_para["value"] = value
        self._label_para["wordstr"] = wordstr
        self._label_para["endindex"] = endindex
        self._label_para["label"] = label
        # logger.debug("[SETLABEL]TRUE :(word)" + wordstr + "(label)" + label + "(value)" + value)
        return result

    # TODO:for price and model the include problem not solved, need to write a func for it
    def set_label(self, inputstr):
        labelrinput = inputstr
        labelinput = inputstr
        cutlist = tool.cut_no_blank(inputstr)
        endindex = 0

        for index in range(len(cutlist)):
            if index < endindex:
                continue
            word = cutlist[index]
            result = self.classify_word(word, cutlist[index:])
            if result:
                labelrinput = labelrinput.replace(self._label_para["wordstr"], self._label_para["label"], 1)
                labelinput = labelinput.replace(self._label_para["wordstr"], self._label_para["label"] + " "
                                                + self._label_para["value"] + " ", 1)
                endindex = index + self._label_para["endindex"] + 1

        return labelinput, labelrinput

    def search(self, labelrinput):
        score = {"score": 0, "index": 0}
        for index, row in self.patterndf.iterrows():
            question = row["question"]
            tmpscore = fuzz.ratio(question, labelrinput)
            if tmpscore > score["score"]:
                score["score"] = tmpscore
                score["index"] = index
            # TODO：improve log.py support showing specific log
            # logger.debug("labelrquestion is " + str(labelrquestion))
            # logger.debug("tmpscore is " + str(tmpscore))

        logger.debug("[PATTERN]most likely pattern is " + self.patterndf["question"][score["index"]])
        logger.debug("[PATTERN]pattern max score is " + str(score["score"]))

        if score["score"] > 50:
            return self.patterndf["category"][score["index"]]
        else:
            return None

    def pattern_welcome(self, inputstr):
        return "WELCOME"

    def pattern_query(self, labelinput):
        inputl = tool.cut_no_blank(labelinput)
        output = "QUERY "
        outputl = []
        for word in inputl:
            strindex = inputl.index(word)
            result, index, _, _ = tool.df_inlude_search(self.querydf, inputl[strindex:], "value", False)
            if result:
                logger.debug("[QUERY]word：" + word + " query label is " + self.querydf["label"][index])
                outputl = tool.insert_list_norepeat(outputl, self.querydf["label"][index])
        output += json.dumps(outputl)
        return output

    def pattern_search(self, labelinput):
        inputl = tool.cut(labelinput)
        output = "SEARCH "
        outputd = {}
        for index in range(len(inputl)):
            word = inputl[index]
            if word in self.searchdf["label"].values:
                outputd[word] = "".join(inputl[index+2: (index+2+inputl[index + 2:].index(" "))])
        output += json.dumps(outputd)
        return output

    def pattern_fuzzyquery(self, labelinput):
        pass

    def pattern_searchquery(self, labelinput):
        pass

    def pattern_compare(self, labelinput):
        pass

    def pattern_para(self, labelinput):
        inputl = tool.cut(labelinput)
        output = "PARA "
        outputd = {}
        for index in range(len(inputl)):
            word = inputl[index]
            if word in self.searchdf["label"].values:
                outputd[word] = "".join(inputl[index+2: (index+2+inputl[index + 2:].index(" "))])
        output += json.dumps(outputd)
        return output

    def gen_output(self, pattern, labelinput):
        gen_func = self.gen_funclist[pattern]
        return gen_func(labelinput)

    # -------------------------------------------------------------
    # function: normalize inputstr
    # args: input -- inputstr
    # return: output -- normalized input
    # -------------------------------------------------------------
    def normalize(self, inputstr):
        logger.info("[NORMALIZE]input: " + inputstr)

        try:
            labelinput, labelrinput = self.set_label(inputstr)
        except Exception as e:
            logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
            log.log_traceback()
            return
        logger.info("[NORMALIZE]input_with_label: " + labelinput)
        logger.info("[NORMALIZE]input_repl_label: " + labelrinput)

        try:
            pattern = self.search(labelrinput)
        except Exception as e:
            logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
            log.log_traceback()
            return
        logger.info("[NORMALIZE]pattern: " + unicode(pattern))
        if pattern is None:
            return inputstr

        try:
            output = self.gen_output(pattern, labelinput)
        except Exception as e:
            logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
            log.log_traceback()
            return

        logger.info("[NORMALIZE]normalize to aiml: " + str(output))
        return output

if __name__ == "__main__":
    # for test
    analyze = Analyze({})

