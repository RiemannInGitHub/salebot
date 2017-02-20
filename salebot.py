# -*- coding: utf-8 -*-
# !/usr/bin/env python
import aimlcov.aimlbrain as aimlbrain
import analyze
import database
import car
import user
import os
import json
import re
import copy
import aimlcov.tuling as tuling
from macro import *
from util import log

logger = log.get_logger(__name__)


# the relationship between salebot, users and cars:
# a salebot is create by server
# a salebot like a host, can handle one user or multi users
# multi users like a chat room, no clearly design yet
# a salebot has one car to identify from db, the history find car can be saved in carlist attr
# each user has a carlist attr to remember what car has been watched before
# car contains the search para and search result, only search para be saved in carlist
class SaleBot(object):
    def __init__(self, userid=None, carid=None,
                 aimlpath=os.path.split(os.path.realpath(__file__))[0] + "/aimlcov/load_aiml.xml"):
        self.__aiml = aimlbrain.AimlBrain(aimlpath)
        self.user = user.User(userid)
        self.users = []
        self.analyze = analyze.Analyze()
        self.database = database.Database()
        self.attrlist = self.database.generate_attrlist()
        self.car = car.Car(self.attrlist, carid)
        self.carlist = []
        self.tuling = tuling.TulingBot()
        self.genargflag = False
        self.consernarg = []
        self.msgregex = re.compile('\{.+\}')
        self.msgfunclist = {
            "SET":      self.msg_set_handle,
            "QUERY":    self.msg_query_handle,
            "DBSEARCH": self.msg_dbsearch_handle,
        }
        logger.info("salebot start")

    def msg_set_handle(self, msg):
        for label, value in msg.items():
            self.car.parad[label] = value

    def msg_query_handle(self, keyl):
        output = ""
        for key in keyl:
            lenth, value = self.database.get_label_value(key, self.car.result)
            if 0 == lenth:
                raise ValueError
            elif 1 == lenth:
                output += self.__aiml.respond_with_viable([key, value[0]], DIALOG[QUERYFIN]) + ";"
            elif 1 < lenth:
                output += self.__aiml.respond_with_viable([key], DIALOG[MULTIKEY]) + ";"
                carnum, carlist = self.database.get_label_value(CARMODEL, self.car.result)
                output += self.__aiml.respond_with_viable([carnum], DIALOG[CARNUM]) + ";"
                for index, row in self.car.result.iterrows():
                    cardesc = row[CARBRAND] + row[CARNAME] + row[CARMODEL]
                    cardesc = cardesc.replace(" ", "")
                    vialist = [cardesc, key, row[key]]
                    output += self.__aiml.respond_with_viable(vialist, DIALOG[MULTIRESULT]) + ";"
        return output

    def msg_tuling_handle(self, msg):
        return self.tuling.tuling_auto_reply(msg)

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

    def process_consernarg(self):
        tmpconsernarg = copy.deepcopy(self.consernarg)
        for k in tmpconsernarg:
            logger.debug("[SEARCH]process_consernarg consernarg is " + str(self.consernarg))
            lenth, value = self.database.get_label_value(k, self.car.result)
            logger.debug("[SEARCH]key " + k + " in database lenth is " + str(lenth) + " value is " + str(value))
            if 0 == lenth:
                raise ValueError
            if PRICE == k or CARMODEL == k:
                if lenth < 5:
                    # self.set_car_para(k, value[0])
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
        self.car.result = self.database.query_by_condition(self.car.parad, self.genargflag, self.car.result)
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
        elif response.find("TULING") != -1:
            response = response.replace("TULING", "", 1)
            output = self.msg_tuling_handle(response)
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
        normalinput = self.analyze.normalize(inputstr)
        if normalinput is None:
            logger.error("in respond the normalinput is None")
            return ""

        output = self.respond_analyze(self.__aiml.respond(normalinput))
        logger.info("final output: " + output)
        # TODO: output has 3 parts: userid, retcode, answer string
        return output


if __name__ == "__main__":
    # for test
    salerobot = SaleBot()
    while(1):
        print(salerobot.respond(raw_input(">>>>")))


