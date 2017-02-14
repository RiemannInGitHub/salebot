# !/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba as jb
import re

num_re = re.compile('\d+')
year_re = re.compile('20\d{2}')
num_dict = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
label_dict = {"<y>": year_re, "<d>": num_re}


def label_process(string):
    for k, v in num_dict.iteritems():
        string = string.replace(k, v)
    for label, regex in label_dict.iteritems():
        string = regex.sub(label, string)
    return string


# paraflag-true: sensitive to the para; false: no sensitive to the para
def df_inlude_search(df, strlist, column, paraflag):
    result = False
    index = 0
    wordstr = ""
    for valuestr in df[column].values:
        cmpword = ""
        labelcmpword = ""
        labelvalue = paraflag and valuestr or label_process(valuestr)
        for word in strlist:
            cmpword += word
            labelword = paraflag and valuestr or label_process(word)
            labelcmpword += labelword
            if not labelvalue.find(labelcmpword):
                break
            if labelcmpword == labelvalue:
                result = True
                break
        if result:
            index = df[column].values.index(valuestr)
            wordstr = cmpword
            break
    return result, index, wordstr


def cut_no_blank(string):
    cutgen = jb.cut(string)
    cutlist = []
    for i in cutgen:
        if i != " ":
            cutlist.append(i)
    return cutlist


def cut(string):
    cutgen = jb.cut(string)
    cutlist = []
    for i in cutgen:
        cutlist.append(i)
    return cutlist


def insert_list_norepeat(li, value):
    if value not in li:
        li.append(value)
    return li

if __name__ == "__main__":
    # for test
    while(1):
        print(label_process(raw_input(">>>")))
