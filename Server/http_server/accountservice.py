import sys
sys.path.append("../util")
import dao, daoconfig
from comm import *
from util import *
import json

class accountservice(object):
    def __init__(self):
        print "in accountservice"
        config = daoconfig.DBConfig("../util/a.conf")
        self.__dao = dao.AccountDao(config)

    def __account2json(self, account):
        for i, j in account.vars(self).items():
            print i, j
        json_buffer = ""

    def get(self, request, headers):
        query_dict = request.query_dict

        try:
            ret, acct = self.__dao.getAccount(int(query_dict["cid"]))
            json_ret = json.dumps(acct.__dict__)
            return json_ret
        except Exception, e:
            print str(e)
        

    def register(self):
        pass

