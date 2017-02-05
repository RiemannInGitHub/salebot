# -*- coding: utf-8 -*

DICT = {
    u'CARBRAND': [u'长安', u'奔驰', u'马自达', u'奥迪'],
    u'CARMODEL': [u'C15', u'C35', u'C75'],
}

CAR_NAME = [u'长安', u'奔驰', u'马自达', u'奥迪']
MODEL = [u'C15', u'C35', u'C75']

DIALOG = {
    u'pickonecar': u'请问您想看具体哪一种型号的车？',
    u'onlyshowonecar': u'不能同时看多辆车哦，屏幕一次展示一辆车。请问具体看哪一辆？',
}

AIMLVAR = [u'carbrand', u'carmodel', u'userkey']

USERKEY = u'userkey'
CARBRAND = u'carbrand'
CARMODEL = u'carmodel'

PATTERN = {
    u'看车': [{u'CARBRAND': 1, u'CARMODEL': 1, u'看': 0.3, u'我': 0.3, u'怎么样': 0.3}, [u'看车', u'CARBRAND', u'CARMODEL']]
}

PTTHRESHOLD = 2.2
