# -*- coding: utf-8 -*

USERKEY = "userkey"

# DB Attr Key_value
CARBRAND = "CARBRAND"
CARNAME = "CARNAME"
CARMODEL = "CARMODEL"
PRICE = "PRICE"
TYPE = "TYPE"
SEATS = "SEATS"

# dialog key
SEARCHFIN = "SEARCHFIN"
QUERYFIN = "QUERYFIN"

DIALOG = {
    CARBRAND: "ASK CARBRAND",
    CARNAME: "ASK CARNAME",
    CARMODEL: "ASK CARMODEL",
    PRICE: "ASK PRICE",
    TYPE: "ASK TYPE",
    SEATS: "ASK SEATS",
    SEARCHFIN: "SEARCH FIN",
    QUERYFIN: "QUERY FIN KEY * VALUE *",
}

AIMLVAR = ["carbrand", "carmodel", "userkey"]


PATTERN = {
    u"看车": [{u"CARBRAND": 1, u"CARMODEL": 1, u"看": 0.3, u"我": 0.3, u"怎么样": 0.3}, [u"看车", u"CARBRAND", u"CARMODEL"]],
    u"SEARCH": [{u"CARBRAND": 1, u"CARNAME": 1, u"CARMODEL": 1, u"PRICE": 1, u"TYPE": 1, u"SEATS": 1},
                [u"SEARCH", u"CARBRAND", u"CARNAME", u"CARMODEL", u"PRICE", u"TYPE", u"SEATS"]],
    u"QUERY": [{u"PRICE": 1, u"ENGINE": 1, u"GEARBOX": 1, u"OILCONSUMPTION": 1, u"ROZ": 1},
               [u"QUERY", u"*"]],  # QUERY可以重复多次，对于一句查询多条信息的，分多次query执行返回结果，如果前面的有打断，则放弃后面的执行
}

ARGORDER = [[u"CARBRAND", u"CARNAME", u"CARMODEL", u"PRICE", u"TYPE", u"SEATS"],
            [u"PRICE", u"TYPE", u"SEATS", u"CARBRAND", u"CARNAME", u"CARMODEL", ]]

