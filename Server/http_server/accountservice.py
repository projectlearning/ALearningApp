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
            if ret == 0:
                ret_dict = {
                    "userid": userinfo.UserID,
                    "responseStr":"Success"
                    }
            else:
                ret_dict = {
                    "responseStr":"Register_failed"
                    }
            json_ret = json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)

    def user_login(self, request, headers):
        query_dict = request.form
        try:
            ret, acct = self.__dao.get_user(str(query_dict["phonenum"]))
            print ret, acct.PhoneNum, acct.Password
            if acct.PhoneNum == query_dict["phonenum"] and acct.Password == query_dict["password"]:
                ret_dict = {
                    "responseStr":"Success"

                    }
            else:
                ret_dict = {
                    "responseStr":"Login_Fail"
                        }
            json_ret = json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)

    def user_get(self, request, headers):
        query_dict = request.query_dict
        try:
            ret, acct = self.__dao.get_user(str(query_dict["userid"]))
            if ret == 0:
                ret_dict = {
                    "responseStr":"Success"
                    }
                ret_dict[]
            else:
                ret_dict = {
                    "responseStr":"Login_Fail"
                        }
            json_ret = json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)


    def user_update(self, request, headers):
        query_dict = request.form
        try:
            ret, user_info = self.__dao.get_user(int(query_dict["userid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            if query_dict.get("userid") != None:
                user_info.UserID = long(query_dict.get("userid"))
            if query_dict.get("phonenum") != None:
                user_info.PhoneNum = str(query_dict.get("phonenum"))
            if query_dict.get("password") != None:
                user_info.Password = str(query_dict.get("password"))
            if query_dict.get("username") != None:
                user_info.Username = str(query_dict.get("username"))
            if query_dict.get("email") != None:
                user_info.Email = str(query_dict.get("email"))
            if query_dict.get("token") != None:
                user_info.Token = str(query_dict.get("token"))
            if query_dict.get("firstname") != None:
                user_info.FirstName = str(query_dict.get("firstname"))
            if query_dict.get("lastname") != None:
                user_info.LastName = str(query_dict.get("lastname"))
            if query_dict.get("profilephotourl") != None:
                user_info.ProfilePhotoURL = str(query_dict.get("profilephotourl"))
            if query_dict.get("usertype") != None:
                user_info.UserType = int(query_dict.get("usertype"))
            if query_dict.get("academicqualification") != None:
                user_info.AcademicQualification = int(query_dict.get("academicqualification"))
            if query_dict.get("experienceinyears") != None:
                user_info.ExperienceInYears = int(query_dict.get("experienceinyears"))
            if query_dict.get("graduatefrom") != None:
                user_info.GraduateFrom = str(query_dict.get("graduatefrom"))
            if query_dict.get("idcardverification") != None:
                user_info.IDCardVerification = int(query_dict.get("idcardverification"))
            if query_dict.get("teachercertifeverification") != None:
                user_info.TeacherCertifeVerification = int(query_dict.get("teachercertifeverification"))
            if query_dict.get("graduationcertificateverification") != None:
                user_info.GraduationCertificateVerification = int(query_dict.get("graduationcertificateverification"))
            if query_dict.get("totalnumofclassinhours") != None:
                user_info.TotalNumOfClassInHours = int(query_dict.get("totalnumofclassinhours"))
            if query_dict.get("totalnumofclassintimes") != None:
                user_info.TotalNumOfClassInTimes = int(query_dict.get("totalnumofclassintimes"))
            if query_dict.get("overallrate") != None:
                user_info.OverallRate = float(query_dict.get("overallrate"))
            if query_dict.get("goodrate") != None:
                user_info.GoodRate = float(query_dict.get("goodrate"))
            if query_dict.get("addressforclass") != None:
                user_info.AddressForClass = str(query_dict.get("addressforclass"))
            ret = self.__dao.update_user(user_info)
            if ret == 0:
                ret_dict = {"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Update_failed"}
            json.dums(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
