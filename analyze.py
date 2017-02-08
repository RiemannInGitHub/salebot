# !/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba as jb
from macro import *


class Analyze(object):
    def __init__(self, attrdict):
        self.attrdict = attrdict

    # -------------------------------------------------------------
    # function: set labels in an input
    # args: input -- inputstr eg: "长安c15"
    # return: output -- input with labels eg: "carbrand长安<carmodel>c15"
    # -------------------------------------------------------------
    def set_label(self, inputstr):
        output = ""
        result = jb.cut(inputstr)
        for word in result:
            label = [k for k, v in self.attrdict.iteritems() if word in v.values()]
            if len(label) != 0:
                output = output + ' ' + label.pop() + ' '
            output = output + word
        return output

    # -------------------------------------------------------------
    # function: normalize inputstr
    # args: input -- inputstr
    # return: output -- normalized input
    # -------------------------------------------------------------
    def normalize(self, inputstr):
        fenci = jb.cut(inputstr)
        score = {}
        labels = {}
        outputl = []

        for pattern, value in PATTERN.iteritems():
            score[pattern] = 0
            for word in fenci:
                if word in value[0].keys():
                    score[pattern] = score[pattern] + value[0][word]
                if word in self.attrdict.keys():
                    for w in fenci:
                        if w != ' ':
                            labels[word] = w
                            break

        sorted(score.iteritems(), key=lambda d: d[1], reverse=True)

        k = score.keys()[0]
        v = score[k]
        if v > PTTHRESHOLD:
            for word in PATTERN[k][1]:
                if word in labels.keys():
                    outputl.append(word)
                    outputl.append(labels[word])
                else:
                    outputl.append(word)
            outputstr = " ".join(outputl)
        else:
            outputstr = inputstr

        return outputstr

if __name__ == "__main__":
    # for test
    pass
