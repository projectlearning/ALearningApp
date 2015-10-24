import daoconfig
import dao
from comm import *


a = daoconfig.DBConfig("a.conf")
#a.printseg()

#print a.getItem("DataBase", "ip")
print a.getIp()
print a.getPasswd()

dao = dao.AccountDao(a)
acct = account(1, "ison", "m", 20)
ret = dao.addAccount(acct)

print "add account ret", ret

