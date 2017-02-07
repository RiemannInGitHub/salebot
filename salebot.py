# -*- coding: utf-8 -*-
# !/usr/bin/env python
import aimlcov
import analyze
import knowledge
import car
import os
import json
import re
from macro import *


class SaleBot(object):
    def __init__(self, userkey=None, currentcar=None,
                 aimlpath=os.path.split(os.path.realpath(__file__))[0] + "/aimlcov/load_aiml.xml"):
        self.__aiml = aimlcov.AimlBrain(aimlpath)
        self.username = ""
        self.userkey = userkey
        self.carlist = []
        self.car = car.Car()
        self.database = knowledge.Database()
        self.consernarg = []
        self.msgregex = re.compile('\{.+\}')
        self.msgfunclist = {
            u'SET':      self.msg_set_handle,
            u'QUERY':    self.msg_query_handle,
            u'DBSEARCH': self.msg_dbsearch_handle,
        }

    def msg_set_handle(self, msg):
        for label, value in msg.items():
            self.car.parad[label] = value

    def msg_query_handle(self, key):
        lenth, value = self.database.get_label_value(key)
        if 0 == lenth:
            raise "msg_query_handle: something goes wrong, the dbresult is NULL"
        elif 1 == lenth:
            vialist = [key, value]
            self.__aiml.respond_with_viable(vialist, DIALOG[QUERYFIN])
        elif 1 < lenth:
            if PRICE == key:
                pass

    def gen_consernarg(self, label):
        if len(self.consernarg) != 0:
            return
        if CARBRAND == label:
            self.consernarg = ARGORDER[0]
        elif CARNAME == label:
            self.consernarg = ARGORDER[0]
        elif CARMODEL == label:
            self.consernarg = ARGORDER[0]
        elif PRICE == label:
            self.consernarg = ARGORDER[1]
        elif TYPE == label:
            self.consernarg = ARGORDER[1]
        elif SEATS == label:
            self.consernarg = ARGORDER[1]

    def set_car_para(self, label, value):
        self.car.parad[label] = value

    def query_car_db(self):
        self.database.query_by_condition(self.car.parad)

    def process_consernarg(self):
        for k in self.consernarg:
            lenth, value = self.database.get_label_value(k)
            if 0 == lenth:
                raise "process_consernarg: something goes wrong, the dbresult is NULL"
            if PRICE == k or MODEL == k:
                if lenth < 5:
                    self.set_car_para(k, value[0])
                    self.consernarg.remove(k)
            elif 1 == lenth:
                self.set_car_para(k, value[0])
                self.consernarg.remove(k)

    def msg_dbsearch_handle(self, msg):
        for label, value in msg.items():
            if value != "":
                self.gen_consernarg(label)
                self.set_car_para(label, value)
                self.__aiml.save_viable(label, value)
        self.query_car_db()
        self.process_consernarg()
        if 0 == len(self.consernarg):
            return self.__aiml.respond(DIALOG[SEARCHFIN])
        keyword = self.consernarg[0]
        return self.__aiml.respond(DIALOG[keyword])

    # -------------------------------------------------------------
    # function: receive msg from aiml to remember sth
    # args: response -- response
    # return:
    # describe: aiml is an independent module, so by sendmsg to remember sth from it
    # -------------------------------------------------------------
    def respond_analyze(self, response):
        m = self.msgregex.match(response)
        output = ""

        if m is not None:
            text = response[m.end():]
            string = m.group()
            msg = json.loads(string)
            for msgtype in msg.keys():
                handlefunc = self.msgfunclist[msgtype]
                output = handlefunc(msg[msgtype])
                if output is None:
                    output = text
        else:
            output = response

        return output

    # -------------------------------------------------------------
    # function: construct output for user's input
    # args: input -- input
    # return: output -- input
    # describe: there are few steps for progressing
    #           1) normalize input or transform input to robot recognise pattern
    #           2) find direct answer from knowledge (no use temp)
    #           3) aiml progressing
    #           4) analyze aiml respond for robot thinking
    # -------------------------------------------------------------
    def respond(self, inputstr):
        labelinput = analyze.set_label(inputstr)
        normalinput = analyze.normalize(labelinput)
        return self.respond_analyze(self.__aiml.respond(normalinput))


if __name__ == "__main__":
    # for test
    salerobot = SaleBot()
    while(1):
        print(salerobot.respond(raw_input(">")))


