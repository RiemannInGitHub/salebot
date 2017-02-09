# !/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba as jb


def df_inlude_search(df, value, column):
    result = False
    index = 0
    for string in df[column].values:
        strlist = string.splite(',')
        if value in strlist:
            result = True
            break
        index += 1
    return result, index


def cut_no_blank(string):
    cutgen = jb.cut(string)
    cutlist = []
    for i in cutgen:
        if i != " ":
            cutlist.append(i)
    return cutlist

