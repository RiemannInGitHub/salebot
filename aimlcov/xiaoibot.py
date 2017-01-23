#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "third_party/")
import xiaoi

# please input your key/sec
test_key = "CgN6QllypQAf"
test_sec = "2bih63ppAGnsTyR5tPuo"

assert len(sys.argv) > 1

text = sys.argv[1]

signature_ask = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                                 app_sec=test_sec,
                                                 uri="/ask.do",
                                                 http_method="POST")

params_ask = xiaoi.ibotcloud.AskParams(platform="custom",
                                          user_id="abc",
                                          url="http://nlp.xiaoi.com/ask.do",
                                          response_format="xml")

ask_session = xiaoi.ibotcloud.AskSession(signature_ask, params_ask)

# demo how to get answer
ret_ask = ask_session.get_answer(text)

print 'i' + ret_ask.http_body
