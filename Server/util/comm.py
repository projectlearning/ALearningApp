import sys

DB_OK = 0
DB_GET_FAIL = -10001
DB_ADD_FAIL = -10002
DB_UPDATE_FAIL = -10003
DB_DEL_FAIL = -10004

class account:
    def __init__(self, cid = 0, nickname = "", sex = "", age = 0):
        self.cid = cid
        self.nickname = nickname
        self.sex = sex
        self.age = age

