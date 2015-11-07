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

            userinfo = User(Username=username, PhoneNum=phonenum, Password=password, Email=email)
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
            ret, acct = self.__dao.get_user_by_phonenum(str(query_dict["phonenum"]))
            if ret == 0:
                print "user_login ret: %d phonenum: %s pwd: %s" % (ret, acct.PhoneNum, acct.Password)
            else: 
                print "the phonenum can't find"
            if ret == 0 and acct.PhoneNum == query_dict["phonenum"] and acct.Password == query_dict["password"]:
                ret_dict = {
                    "responseStr":"Success"

                    }
                ret_dict["userid"] = acct.UserID
            else:
                ret_dict = {
                    "responseStr":"Login_Fail"
                        }
            json_ret = json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Register__failed"}
            json_ret = json.dumps(ret_dict)
            return json_ret

    def user_update(self, request, headers):
        query_dict = request.form
        #print query_dict
        try:
            if query_dict.get("userid", None) is None:
                print "not userid"
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            ret, user_info = self.__dao.get_user_by_userid(int(query_dict["userid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            print query_dict
            if query_dict.get("userid") != None:
                user_info.UserID = (query_dict.get("userid"))
            if query_dict.get("phonenum") != None:
                user_info.PhoneNum = (query_dict.get("phonenum"))
            if query_dict.get("password") != None:
                user_info.Password = (query_dict.get("password"))
            if query_dict.get("username") != None:
                user_info.Username = (query_dict.get("username"))
            if query_dict.get("email") != None:
                user_info.Email = (query_dict.get("email"))
            if query_dict.get("token") != None:
                user_info.Token = (query_dict.get("token"))
            if query_dict.get("firstname") != None:
                user_info.FirstName = (query_dict.get("firstname"))
            if query_dict.get("lastname") != None:
                user_info.LastName = (query_dict.get("lastname"))
            if query_dict.get("profilephotourl") != None:
                user_info.ProfilePhotoURL = (query_dict.get("profilephotourl"))
            if query_dict.get("usertype") != None:
                user_info.UserType = (query_dict.get("usertype"))
            if query_dict.get("academicqualification") != None:
                user_info.AcademicQualification = (query_dict.get("academicqualification"))
            if query_dict.get("experienceinyears") != None:
                user_info.ExperienceInYears = (query_dict.get("experienceinyears"))
            if query_dict.get("graduatefrom") != None:
                user_info.GraduateFrom = (query_dict.get("graduatefrom"))
            if query_dict.get("idcardverification") != None:
                user_info.IDCardVerification = (query_dict.get("idcardverification"))
            if query_dict.get("teachercertifeverification") != None:
                user_info.TeacherCertifeVerification = (query_dict.get("teachercertifeverification"))
            if query_dict.get("graduationcertificateverification") != None:
                user_info.GraduationCertificateVerification = (query_dict.get("graduationcertificateverification"))
            if query_dict.get("totalnumofclassinhours") != None:
                user_info.TotalNumOfClassInHours = (query_dict.get("totalnumofclassinhours"))
            if query_dict.get("totalnumofclassintimes") != None:
                user_info.TotalNumOfClassInTimes = (query_dict.get("totalnumofclassintimes"))
            if query_dict.get("overallrate") != None:
                user_info.OverallRate = (query_dict.get("overallrate"))
            if query_dict.get("goodrate") != None:
                user_info.GoodRate = (query_dict.get("goodrate"))
            if query_dict.get("addressforclass") != None:
                user_info.AddressForClass = (query_dict.get("addressforclass"))
            ret = self.__dao.update_user(user_info)
            if ret == 0:
                ret_dict = {"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Update_failed"}
            json_ret = json.dumps(ret_dict)
            #json_ret = ret_dict
            return json_ret
        except Exception, e:
            print str(e)  + getTraceStackMsg()
            ret_dict = {"responseStr":"Update_failed"}
            json_ret = json.dumps(ret_dict)
            return json_ret
    def user_get(self, request, headers):
        query_dict = request.query_dict
        try:
            ret, user_info = self.__dao.get_user_by_userid(int(query_dict["userid"]))
            if ret != 0:
                ret_dict = {"responseStr":"get_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            ret_dict["userid"] =str( user_info.UserID)
            ret_dict["phonenum"] =str( user_info.PhoneNum)
            ret_dict["password"] =str( user_info.Password)
            ret_dict["username"] =str( user_info.Username)
            ret_dict["email"] =str( user_info.Email)
            ret_dict["token"] =str( user_info.Token)
            ret_dict["firstname"] =str( user_info.FirstName)
            ret_dict["lastname"] =str( user_info.LastName)
            ret_dict["profilephotourl"] =str( user_info.ProfilePhotoURL)
            ret_dict["usertype"] =str( user_info.UserType)
            ret_dict["academicqualification"] =str( user_info.AcademicQualification)
            ret_dict["experienceinyears"] =str( user_info.ExperienceInYears)
            ret_dict["graduatefrom"] =str( user_info.GraduateFrom)
            ret_dict["idcardverification"] =str( user_info.IDCardVerification)
            ret_dict["teachercertifeverification"] =str( user_info.TeacherCertifeVerification)
            ret_dict["graduationcertificateverification"] =str( user_info.GraduationCertificateVerification)
            ret_dict["totalnumofclassinhours"] =str( user_info.TotalNumOfClassInHours)
            ret_dict["totalnumofclassintimes"] =str( user_info.TotalNumOfClassInTimes)
            ret_dict["overallrate"] =str( user_info.OverallRate)
            ret_dict["goodrate"] =str( user_info.GoodRate)
            ret_dict["addressforclass"] =str( user_info.AddressForClass)
            json_ret =json.dumps(ret_dict)
            #json_ret = ret_dict
            print json_ret
            return json_ret
        except Exception, e:
            print str(e) + getTraceStackMsg()
            ret_dict = {"responseStr":"get__failed"}
            json_ret = json.dumps(ret_dict)
            return json_ret
