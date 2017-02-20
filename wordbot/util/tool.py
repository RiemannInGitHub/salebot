# !/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba as jb
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

num_re = re.compile('\d+')
year_re = re.compile('20\d{2}')
num_dict = {u"一": "1", u"二": "2", u"三": "3", u"四": "4", u"五": "5", u"六": "6", u"七": "7", u"八": "8", u"九": "9"}
label_dict = {"<y>": year_re, "<d>": num_re}


# TODO: add a new func to change to num
def num_process(string):
    for k, v in num_dict.iteritems():
        string = string.replace(k, v)
    return string


def label_process(string):
    string = num_process(string)
    for label, regex in label_dict.iteritems():
        string = regex.sub(label, string)
    return string


# paraflag-true: sensitive to the para; false: no sensitive to the para
def df_inlude_search(df, strlist, column, paraflag):
    result = False
    index = 0
    wordstr = ""
    strindex = 0

    for index, row in df.iterrows():
        cmpword = ""
        labelcmpword = ""
        valuestr = row[column]
        labelvalue = paraflag and valuestr or label_process(valuestr)
        for strindex in range(len(strlist)):
            word = strlist[strindex]
            cmpword += word
            labelword = paraflag and valuestr or label_process(word)
            labelcmpword += labelword
            if labelvalue.find(labelcmpword) is -1:
                break
            if labelcmpword == labelvalue:
                result = True
                wordstr = valuestr
                break
        if result:
            wordstr = cmpword
            break

    return result, index, wordstr, strindex


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
