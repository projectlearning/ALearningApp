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
        try:
            ret, user_info = self.__dao.get_user_by_userid(int(query_dict["userid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            print query_dict
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
            json_ret = json.dumps(ret_dict)
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
            ret_dict["userid"] = user_info.UserID
            ret_dict["phonenum"] = user_info.PhoneNum
            ret_dict["password"] = user_info.Password
            ret_dict["username"] = user_info.Username
            ret_dict["email"] = user_info.Email
            ret_dict["token"] = user_info.Token
            ret_dict["firstname"] = user_info.FirstName
            ret_dict["lastname"] = user_info.LastName
            ret_dict["profilephotourl"] = user_info.ProfilePhotoURL
            ret_dict["usertype"] = user_info.UserType
            ret_dict["academicqualification"] = user_info.AcademicQualification
            ret_dict["experienceinyears"] = user_info.ExperienceInYears
            ret_dict["graduatefrom"] = user_info.GraduateFrom
            ret_dict["idcardverification"] = user_info.IDCardVerification
            ret_dict["teachercertifeverification"] = user_info.TeacherCertifeVerification
            ret_dict["graduationcertificateverification"] = user_info.GraduationCertificateVerification
            ret_dict["totalnumofclassinhours"] = user_info.TotalNumOfClassInHours
            ret_dict["totalnumofclassintimes"] = user_info.TotalNumOfClassInTimes
            ret_dict["overallrate"] = user_info.OverallRate
            ret_dict["goodrate"] = user_info.GoodRate
            ret_dict["addressforclass"] = user_info.AddressForClass
            json_ret = json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e) + getTraceStackMsg()
            ret_dict = {"responseStr":"get__failed"}
            json_ret = json.dumps(ret_dict)
            return json_ret
