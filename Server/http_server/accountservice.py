import sys
sys.path.append("../util")
import dao, daoconfig
from comm import *
from util import *
import json

class accountservice(object):
    def __init__(self, conf = ""):
        print "in accountservice"
        if conf == "":
            conf = "../util/alearning.conf";
        print conf
        config = daoconfig.DBConfig(conf)
        self.__dao = dao.AccountDao(config)

    def __account2json(self, account):
        for i, j in account.vars(self).items():
            print i, j
        json_buffer = ""

    def get_client(self, request, headers):
        query_dict = request.query_dict

        try:
            ret, acct = self.__dao.getAccount(int(query_dict["cid"]))
            json_ret = json.dumps(acct.__dict__)
            return json_ret
        except Exception, e:
            print str(e)
        
    def client_register(self):
        pass  

    def client_login(self):
        pass

    def user_register(self, request, headers):
        query_dict = request.form
        print "user_register: %s" % str(query_dict)
        try:
            username = query_dict.get('username', '')
            phonenum = query_dict.get('phonenum', '')
            password = query_dict.get('password', '')
            email = query_dict.get('email', '')

            userinfo = user(Username=username, PhoneNum=phonenum, Password=password, Email=email)
            ret = self.__dao.add_user(userinfo)
            ret_dict = {
                    "responseStr":"Success"

                    }
            json_ret = json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)

    def user_login(self):
        query_dict = request.query
        try:
            ret, acct = self.__dao.getAccount(int(query_dict["cid"]))
            json_ret = json.dumps(acct.__dict__)
            return json_ret
        except Exception, e:
            print str(e)
      

