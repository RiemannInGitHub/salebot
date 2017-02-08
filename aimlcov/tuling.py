#!/usr/bin/env python
# coding: utf-8

import json
import requests
import sys
import os

sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0] + "/..")
from util import log

reload(sys)
sys.setdefaultencoding('utf8')


logger = log.get_logger(__name__)


class TulingBot(object):
    def __init__(self, uid = 'wangye'):
        self.tuling_key = "7966c1edc0564272809ca834581826d3"
        self.uid = uid

    def tuling_auto_reply(self, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = self.uid
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " + \
                             k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')

            logger.debug("use tulingbot, answer:" + result)
            return result
        else:
            logger.error("use tulingbot, the tuling key is missing")
            return u"知道啦"


if __name__ == "__main__":
    # for test
    assert len(sys.argv) > 1

    text = sys.argv[1]
    tuling = TulingBot()
    print 'tl' + tuling.tuling_auto_reply(text)
