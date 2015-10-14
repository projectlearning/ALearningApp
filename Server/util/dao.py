import MySQLdb
import sys
sys.path.append("../util")
from comm import *
import log

class AccountDao(object):
    def __init__(self, config):
        print "in accountdao"
        self.logger = log.loginit()
        self.__db = None
        try:
            self.__db = MySQLdb.connect(config.getIp(), config.getUser(), config.getPasswd(), config.getDbname())
            self.__cursor = self.__db.cursor()
        except Exception, e:
            print str(e)

    def __del__(self):
        if self.__db is not None:
                self.__db.close() 

    def getAccount(self, cid):
        sql = "Select * from account where cid = '%d'" % (cid)
        #self.logger.debug("sql: %s" % (sql))
        print sql
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            for row in results:
                nickname = row[1]
                sex = row[2]
                age = int(row[3])
                #print nickname, sex, age
                acct = account(cid, nickname, sex, age)
                #print acct.nickname, acct.sex, acct.age
            return DB_OK, acct
        except Exception, e:
            print str(e)
        return DB_GET_FAIL

    def addAccount(self, account):
        sql = "Insert Into account(cid, nickname, age, sex) Values ('%d', '%s', '%d', '%s')" % (account.cid, account.nickname, account.age, account.sex)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
            print str(e)
        return DB_ADD_FAIL

    def updateAccount(self, account):
        sql = "Update account Set cid = '%d', nickname = '%s', age = '%d', sex = '%s' Where cid = '%d'" % (account.cid, account.nickname, account.age, account.sex, account.cid)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
            print str(e)
        return DB_UPDATE_FAIL

    def delAccount(self, cid):
        sql = "Delete From account where cid = '%d'" % (cid)
        try: 
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
            print str(e)
        return DB_DEL_FAIL

