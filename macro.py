# -*- coding: utf-8 -*

USERKEY = u'userkey'
CARBRAND = u'carbrand'
CARNAME = u'carname'
CARMODEL = u'carmodel'
PRICE = u'price'
TYPE = u'type'
SEATS = u'seats'

SEARCHFIN = u'searchfin'
QUERYFIN = u'queryfin'

KEYDICT = {
    u'CARBRAND': [u'长安', u'奔驰', u'马自达', u'奥迪'],
    u'CARNAME': [u'C15', u'C35', u'C75'],
    u'CARMODEL': [],
    u'PRICE': [],
    u'TYPE': [u'SUV'],
    u'SEATS': [u'5座', u'7座']
}

ATTRIBUTE = {
    u'PRICE': '',
    u'ENGINE': '',
    u'GEARBOX': '',
    u'OILCONSUMPTION': '',
    u'ROZ': '',
}

CAR_NAME = [u'长安', u'奔驰', u'马自达', u'奥迪']
MODEL = [u'C15', u'C35', u'C75']

DIALOG = {
    CARBRAND: u'ASK CARBRAND',
    CARNAME: u'ASK CARNAME',
    CARMODEL: u'ASK CARMODEL',
    PRICE: u'ASK PRICE',
    TYPE: u'ASK TYPE',
    SEATS: u'ASK SEATS',
    SEARCHFIN: u'SEARCH FIN',
    QUERYFIN: u'QUERY FIN KEY * VALUE *',
}

AIMLVAR = [u'carbrand', u'carmodel', u'userkey']


PATTERN = {
    u'看车': [{u'CARBRAND': 1, u'CARMODEL': 1, u'看': 0.3, u'我': 0.3, u'怎么样': 0.3}, [u'看车', u'CARBRAND', u'CARMODEL']],
    u'SEARCH': [{u'CARBRAND': 1, u'CARNAME': 1, u'CARMODEL': 1, u'PRICE': 1, u'TYPE': 1, u'SEATS': 1},
                [u'SEARCH', u'CARBRAND', u'CARNAME', u'CARMODEL', u'PRICE', u'TYPE', u'SEATS']],
    u'QUERY': [{u'PRICE': 1, u'ENGINE': 1, u'GEARBOX': 1, u'OILCONSUMPTION': 1, u'ROZ': 1},
               [u'QUERY', u'*']],  # QUERY可以重复多次，对于一句查询多条信息的，分多次query执行返回结果，如果前面的有打断，则放弃后面的执行
}

PTTHRESHOLD = 2.2

ARGORDER = [[u'CARBRAND', u'CARNAME', u'CARMODEL', u'PRICE', u'TYPE', u'SEATS'],
            [u'PRICE', u'TYPE', u'SEATS', u'CARBRAND', u'CARNAME', u'CARMODEL', ]]

