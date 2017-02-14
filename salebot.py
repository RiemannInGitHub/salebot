# -*- coding: utf-8 -*-
# !/usr/bin/env python
import aimlcov.aimlbrain as aimlbrain
import analyze
import database
import car
import os
import json
import re
import copy
import aimlcov.tuling as tuling
from macro import *
from util import log

logger = log.get_logger(__name__)


class SaleBot(object):
    def __init__(self, userkey=None, currentcar=None,
                 aimlpath=os.path.split(os.path.realpath(__file__))[0] + "/aimlcov/load_aiml.xml"):
        self.__aiml = aimlbrain.AimlBrain(aimlpath)
        self.username = ""
        self.userkey = userkey
        self.carlist = []
        self.analyze = analyze.Analyze()
        self.database = database.Database()
        self.attrlist = self.database.generate_attrlist()
        self.car = car.Car(self.attrlist)
        self.tuling = tuling.TulingBot()
        self.genargflag = False
        self.consernarg = []
        self.msgregex = re.compile('\{.+\}')
        self.msgfunclist = {
            "SET":      self.msg_set_handle,
            "QUERY":    self.msg_query_handle,
            "DBSEARCH": self.msg_dbsearch_handle,
            "TULING":   self.msg_tuling_handle,
        }
        self.special_search = {
            PRICE: self.set_price_search,
            CARMODEL: self.set_model_search,
        }
        logger.info("salebot start")

    def msg_set_handle(self, msg):
        for label, value in msg.items():
            self.car.parad[label] = value

    def msg_query_handle(self, keyl):
        output = ""
        for key in keyl:
            lenth, value = self.database.get_label_value(key)
            if 0 == lenth:
                raise ValueError
            elif 1 == lenth:
                vialist = [key, value[0]]
                output += self.__aiml.respond_with_viable(lenth, vialist, DIALOG[QUERYFIN]) + ";"
            elif 1 < lenth:
                vialist = [key, value]
                output += self.__aiml.respond_with_viable(lenth, vialist, DIALOG[QUERYFINMULTI]) + ";"
        return output

    def msg_tuling_handle(self, msg):
        return 'tl' + self.tuling.tuling_auto_reply(msg)

    def gen_consernarg(self, label, oldflag):
        if len(self.consernarg) != 0:
            return oldflag
        flag = True
        self.car.init_parad()
        if CARBRAND == label:
            self.consernarg = copy.deepcopy(ARGORDER[0])
        elif CARNAME == label:
            self.consernarg = copy.deepcopy(ARGORDER[0])
        elif CARMODEL == label:
            self.consernarg = copy.deepcopy(ARGORDER[0])
        elif PRICE == label:
            self.consernarg = copy.deepcopy(ARGORDER[1])
        elif TYPE == label:
            self.consernarg = copy.deepcopy(ARGORDER[1])
        elif SEATS == label:
            self.consernarg = copy.deepcopy(ARGORDER[1])

        logger.debug("[SEARCH]gen_consernarg: " + str(self.consernarg) + " flag is " + str(flag))
        return flag

    def set_car_para(self, label, value):
        self.car.parad[label] = value

    def set_price_search(self):
        pass

    def set_model_search(self):
        pass

    def process_consernarg(self):
        tmpconsernarg = copy.deepcopy(self.consernarg)
        for k in tmpconsernarg:
            logger.debug("[SEARCH]process_consernarg consernarg is " + str(self.consernarg))
            lenth, value = self.database.get_label_value(k)
            logger.debug("[SEARCH]key " + k + " in database lenth is " + str(lenth) + " value is " + str(value))
            if 0 == lenth:
                raise ValueError
            if PRICE == k or CARMODEL == k:
                if lenth < 5:
                    self.set_car_para(k, value[0])
                    self.consernarg.remove(k)
            elif 1 == lenth:
                self.set_car_para(k, value[0])
                self.consernarg.remove(k)
        logger.debug("[SEARCH]process_consernarg: " + str(self.consernarg))

    def msg_dbsearch_handle(self, msg):
        for label, value in msg.items():
            if value != "":
                self.genargflag = self.gen_consernarg(label, self.genargflag)
                self.set_car_para(label, value)
                self.__aiml.save_viable(label, value)
        self.database.query_by_condition(self.car.parad, self.genargflag)
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
        logger.debug("aiml response: " + unicode(response))
        output = ""

        if m is not None:
            text = response[m.end():]
            string = m.group()
            msg = {}

            # TODO: add a decorator for log exception
            try:
                msg = json.loads(string)
                logger.debug("parse msg is:" + str(msg))
            except Exception as e:
                logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
                log.log_traceback()

            for msgtype in msg.keys():
                handlefunc = self.msgfunclist[msgtype]
                try:
                    output = handlefunc(msg[msgtype])
                except Exception as e:
                    logger.critical("exception: " + unicode(Exception) + ":" + unicode(e))
                    log.log_traceback()
                else:
                    if output is None:
                        output = text
        else:
            output = response

        logger.info("output: " + output)
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
        normalinput = self.analyze.normalize(inputstr)
        if normalinput is None:
            logger.error("in respond the normalinput is None")
            return ""

        return self.respond_analyze(self.__aiml.respond(normalinput))


if __name__ == "__main__":
    # for test
    salerobot = SaleBot()
    while(1):
        print(salerobot.respond(raw_input(">>>>")))


