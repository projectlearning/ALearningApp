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
            ret, acct = self.__dao.get_user_by_phonenum(str(query_dict["phonenum"]))
            if ret == 0:
                print "test1"
                print "user_login ret: %d phonenum: %s pwd: %s" % (ret, acct.PhoneNum, acct.Password)
            else: 
                print "test2"
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
            ret_dict = {"responseStr":"Login__failed"}
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
            if query_dict.get("userid", None) is None:
                print "not userid"
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
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

    def requirement_update(self, request, headers):
        query_dict = request.form
        try:
            if query_dict.get("requirementid", None) is None:
                ret_dict = {"responseStr":"Update_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, requirement_info = self.__dao.get_requirement(int(query_dict["requirementid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            if query_dict.get("requirementid") != None:
                requirement_info.RequirementID = long(query_dict.get("requirementid"))
            if query_dict.get("userid") != None:
                requirement_info.UserID = long(query_dict.get("userid"))
            if query_dict.get("requirementtype") != None:
                requirement_info.RequirementType = int(query_dict.get("requirementtype"))
            if query_dict.get("maxprice") != None:
                requirement_info.MaxPrice = int(query_dict.get("maxprice"))
            if query_dict.get("minprice") != None:
                requirement_info.MinPrice = int(query_dict.get("minprice"))
            if query_dict.get("mode") != None:
                requirement_info.Mode = int(query_dict.get("mode"))
            if query_dict.get("status") != None:
                requirement_info.Status = int(query_dict.get("status"))
            if query_dict.get("postdate") != None:
                requirement_info.PostDate = int(query_dict.get("postdate"))
            ret = self.__dao.update_requirement(requirement_info)
            if ret == 0:
                ret_dict = {"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Update_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Update_failed"}
            return json.dumps(ret_dict)

    def requirement_get(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("requirementid", None) is None:
                ret_dict = {"responseStr":"Add_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, requirement_info = self.__dao.get_requirement(int(query_dict["requirementid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Get_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            ret_dict["requirementid"] = requirement_info.RequirementID
            ret_dict["userid"] = requirement_info.UserID
            ret_dict["requirementtype"] = requirement_info.RequirementType
            ret_dict["maxprice"] = requirement_info.MaxPrice
            ret_dict["minprice"] = requirement_info.MinPrice
            ret_dict["mode"] = requirement_info.Mode
            ret_dict["status"] = requirement_info.Status
            ret_dict["postdate"] = requirement_info.PostDate
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Get_failed"}
            return json.dumps(ret_dict)

    def requirement_add(self, request, headers):
        query_dict = request.form
        try:
            requirement_info = requirement()
            if query_dict.get("requirementid") != None:
                requirement_info.RequirementID = long(query_dict.get("requirementid"))
            if query_dict.get("userid") != None:
                requirement_info.UserID = long(query_dict.get("userid"))
            if query_dict.get("requirementtype") != None:
                requirement_info.RequirementType = int(query_dict.get("requirementtype"))
            if query_dict.get("maxprice") != None:
                requirement_info.MaxPrice = int(query_dict.get("maxprice"))
            if query_dict.get("minprice") != None:
                requirement_info.MinPrice = int(query_dict.get("minprice"))
            if query_dict.get("mode") != None:
                requirement_info.Mode = int(query_dict.get("mode"))
            if query_dict.get("status") != None:
                requirement_info.Status = int(query_dict.get("status"))
            if query_dict.get("postdate") != None:
                requirement_info.PostDate = int(query_dict.get("postdate"))
            ret = self.__dao.add_requirement(requirement_info)
            if ret == 0:
                ret_dict = {"requirementid": requirementinfo.RequirementID,
"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret

    def requirement_del(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("requirementid", None) is None:
                ret_dict = {"responseStr":"Del_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret = self.__dao.del_requirement(int(query_dict["requirementid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Del_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Del_failed"}
            json.dumps(ret_dict)
            return json_ret


    def requirementtime_update(self, request, headers):
        query_dict = request.form
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Update_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, requirementtime_info = self.__dao.get_requirementtime(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            if query_dict.get("id") != None:
                requirementtime_info.ID = long(query_dict.get("id"))
            if query_dict.get("requirementid") != None:
                requirementtime_info.RequirementID = long(query_dict.get("requirementid"))
            if query_dict.get("date") != None:
                requirementtime_info.Date = int(query_dict.get("date"))
            if query_dict.get("period") != None:
                requirementtime_info.Period = int(query_dict.get("period"))
            if query_dict.get("isactive") != None:
                requirementtime_info.IsActive = int(query_dict.get("isactive"))
            ret = self.__dao.update_requirementtime(requirementtime_info)
            if ret == 0:
                ret_dict = {"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Update_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Update_failed"}
            return json.dumps(ret_dict)

    def requirementtime_get(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Add_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, requirementtime_info = self.__dao.get_requirementtime(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Get_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            ret_dict["id"] = requirementtime_info.ID
            ret_dict["requirementid"] = requirementtime_info.RequirementID
            ret_dict["date"] = requirementtime_info.Date
            ret_dict["period"] = requirementtime_info.Period
            ret_dict["isactive"] = requirementtime_info.IsActive
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Get_failed"}
            return json.dumps(ret_dict)

    def requirementtime_add(self, request, headers):
        query_dict = request.form
        try:
            requirementtime_info = requirementtime()
            if query_dict.get("id") != None:
                requirementtime_info.ID = long(query_dict.get("id"))
            if query_dict.get("requirementid") != None:
                requirementtime_info.RequirementID = long(query_dict.get("requirementid"))
            if query_dict.get("date") != None:
                requirementtime_info.Date = int(query_dict.get("date"))
            if query_dict.get("period") != None:
                requirementtime_info.Period = int(query_dict.get("period"))
            if query_dict.get("isactive") != None:
                requirementtime_info.IsActive = int(query_dict.get("isactive"))
            ret = self.__dao.add_requirementtime(requirementtime_info)
            if ret == 0:
                ret_dict = {"id": requirementtimeinfo.ID,
"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret

    def requirementtime_del(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Del_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret = self.__dao.del_requirementtime(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Del_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Del_failed"}
            json.dumps(ret_dict)
            return json_ret

    def course_update(self, request, headers):
        query_dict = request.form
        try:
            if query_dict.get("courseid", None) is None:
                ret_dict = {"responseStr":"Update_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, course_info = self.__dao.get_course(int(query_dict["courseid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            if query_dict.get("courseid") != None:
                course_info.CourseID = long(query_dict.get("courseid"))
            if query_dict.get("grade") != None:
                course_info.Grade = int(query_dict.get("grade"))
            if query_dict.get("name") != None:
                course_info.Name = str(query_dict.get("name"))
            ret = self.__dao.update_course(course_info)
            if ret == 0:
                ret_dict = {"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Update_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Update_failed"}
            return json.dumps(ret_dict)

    def course_get(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("courseid", None) is None:
                ret_dict = {"responseStr":"Add_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, course_info = self.__dao.get_course(int(query_dict["courseid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Get_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            ret_dict["courseid"] = course_info.CourseID
            ret_dict["grade"] = course_info.Grade
            ret_dict["name"] = course_info.Name
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Get_failed"}
            return json.dumps(ret_dict)

    def course_add(self, request, headers):
        query_dict = request.form
        try:
            course_info = course()
            if query_dict.get("courseid") != None:
                course_info.CourseID = long(query_dict.get("courseid"))
            if query_dict.get("grade") != None:
                course_info.Grade = int(query_dict.get("grade"))
            if query_dict.get("name") != None:
                course_info.Name = str(query_dict.get("name"))
            ret = self.__dao.add_course(course_info)
            if ret == 0:
                ret_dict = {"courseid": courseinfo.CourseID,
"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret

    def course_del(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("courseid", None) is None:
                ret_dict = {"responseStr":"Del_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret = self.__dao.del_course(int(query_dict["courseid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Del_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Del_failed"}
            json.dumps(ret_dict)
            return json_ret

    def requirementcourse_update(self, request, headers):
        query_dict = request.form
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Update_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, requirementcourse_info = self.__dao.get_requirementcourse(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            if query_dict.get("id") != None:
                requirementcourse_info.ID = long(query_dict.get("id"))
            if query_dict.get("requirementid") != None:
                requirementcourse_info.RequirementID = long(query_dict.get("requirementid"))
            if query_dict.get("courseid") != None:
                requirementcourse_info.CourseID = long(query_dict.get("courseid"))
            ret = self.__dao.update_requirementcourse(requirementcourse_info)
            if ret == 0:
                ret_dict = {"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Update_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Update_failed"}
            return json.dumps(ret_dict)

    def requirementcourse_get(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Add_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, requirementcourse_info = self.__dao.get_requirementcourse(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Get_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            ret_dict["id"] = requirementcourse_info.ID
            ret_dict["requirementid"] = requirementcourse_info.RequirementID
            ret_dict["courseid"] = requirementcourse_info.CourseID
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Get_failed"}
            return json.dumps(ret_dict)

    def requirementcourse_add(self, request, headers):
        query_dict = request.form
        try:
            requirementcourse_info = requirementcourse()
            if query_dict.get("id") != None:
                requirementcourse_info.ID = long(query_dict.get("id"))
            if query_dict.get("requirementid") != None:
                requirementcourse_info.RequirementID = long(query_dict.get("requirementid"))
            if query_dict.get("courseid") != None:
                requirementcourse_info.CourseID = long(query_dict.get("courseid"))
            ret = self.__dao.add_requirementcourse(requirementcourse_info)
            if ret == 0:
                ret_dict = {"id": requirementcourseinfo.ID,
"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret

    def requirementcourse_del(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Del_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret = self.__dao.del_requirementcourse(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Del_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Del_failed"}
            json.dumps(ret_dict)
            return json_ret

    def addressconfig_update(self, request, headers):
        query_dict = request.form
        try:
            if query_dict.get("addressconfigid", None) is None:
                ret_dict = {"responseStr":"Update_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, addressconfig_info = self.__dao.get_addressconfig(int(query_dict["addressconfigid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            if query_dict.get("addressconfigid") != None:
                addressconfig_info.AddressConfigID = long(query_dict.get("addressconfigid"))
            if query_dict.get("country") != None:
                addressconfig_info.Country = str(query_dict.get("country"))
            if query_dict.get("province") != None:
                addressconfig_info.Province = str(query_dict.get("province"))
            if query_dict.get("city") != None:
                addressconfig_info.City = str(query_dict.get("city"))
            if query_dict.get("district") != None:
                addressconfig_info.District = str(query_dict.get("district"))
            ret = self.__dao.update_addressconfig(addressconfig_info)
            if ret == 0:
                ret_dict = {"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Update_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Update_failed"}
            return json.dumps(ret_dict)

    def addressconfig_get(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("addressconfigid", None) is None:
                ret_dict = {"responseStr":"Add_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, addressconfig_info = self.__dao.get_addressconfig(int(query_dict["addressconfigid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Get_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            ret_dict["addressconfigid"] = addressconfig_info.AddressConfigID
            ret_dict["country"] = addressconfig_info.Country
            ret_dict["province"] = addressconfig_info.Province
            ret_dict["city"] = addressconfig_info.City
            ret_dict["district"] = addressconfig_info.District
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Get_failed"}
            return json.dumps(ret_dict)

    def addressconfig_add(self, request, headers):
        query_dict = request.form
        try:
            addressconfig_info = addressconfig()
            if query_dict.get("addressconfigid") != None:
                addressconfig_info.AddressConfigID = long(query_dict.get("addressconfigid"))
            if query_dict.get("country") != None:
                addressconfig_info.Country = str(query_dict.get("country"))
            if query_dict.get("province") != None:
                addressconfig_info.Province = str(query_dict.get("province"))
            if query_dict.get("city") != None:
                addressconfig_info.City = str(query_dict.get("city"))
            if query_dict.get("district") != None:
                addressconfig_info.District = str(query_dict.get("district"))
            ret = self.__dao.add_addressconfig(addressconfig_info)
            if ret == 0:
                ret_dict = {"addressconfigid": addressconfiginfo.AddressConfigID,
"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret

    def addressconfig_del(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("addressconfigid", None) is None:
                ret_dict = {"responseStr":"Del_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret = self.__dao.del_addressconfig(int(query_dict["addressconfigid"]))
            if ret != 0:
                ret_dict = {"responseStr":"Del_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Del_failed"}
            json.dumps(ret_dict)
            return json_ret

    def address_update(self, request, headers):
        query_dict = request.form
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Update_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, address_info = self.__dao.get_address(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Update_failed"}
                return json.dumps(ret_dict)
            if query_dict.get("id") != None:
                address_info.ID = long(query_dict.get("id"))
            if query_dict.get("requirementid") != None:
                address_info.RequirementID = long(query_dict.get("requirementid"))
            if query_dict.get("userid") != None:
                address_info.UserID = long(query_dict.get("userid"))
            if query_dict.get("addressconfigid") != None:
                address_info.AddressConfigID = long(query_dict.get("addressconfigid"))
            if query_dict.get("restaddress") != None:
                address_info.RestAddress = str(query_dict.get("restaddress"))
            ret = self.__dao.update_address(address_info)
            if ret == 0:
                ret_dict = {"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Update_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Update_failed"}
            return json.dumps(ret_dict)

    def address_get(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Add_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret, address_info = self.__dao.get_address(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Get_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            ret_dict["id"] = address_info.ID
            ret_dict["requirementid"] = address_info.RequirementID
            ret_dict["userid"] = address_info.UserID
            ret_dict["addressconfigid"] = address_info.AddressConfigID
            ret_dict["restaddress"] = address_info.RestAddress
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Get_failed"}
            return json.dumps(ret_dict)

    def address_add(self, request, headers):
        query_dict = request.form
        try:
            address_info = address()
            if query_dict.get("id") != None:
                address_info.ID = long(query_dict.get("id"))
            if query_dict.get("requirementid") != None:
                address_info.RequirementID = long(query_dict.get("requirementid"))
            if query_dict.get("userid") != None:
                address_info.UserID = long(query_dict.get("userid"))
            if query_dict.get("addressconfigid") != None:
                address_info.AddressConfigID = long(query_dict.get("addressconfigid"))
            if query_dict.get("restaddress") != None:
                address_info.RestAddress = str(query_dict.get("restaddress"))
            ret = self.__dao.add_address(address_info)
            if ret == 0:
                ret_dict = {"id": addressinfo.ID,
"responseStr":"Success"}
            else:
                ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Add_failed"}
            json.dumps(ret_dict)
            return json_ret

    def address_del(self, request, headers):
        query_dict = request.query_dict
        try:
            if query_dict.get("id", None) is None:
                ret_dict = {"responseStr":"Del_failed"}
                json.dumps(ret_dict)
                return json_ret
            ret = self.__dao.del_address(int(query_dict["id"]))
            if ret != 0:
                ret_dict = {"responseStr":"Del_failed"}
                return json.dumps(ret_dict)
            ret_dict = {"responseStr":"Success"}
            json.dumps(ret_dict)
            return json_ret
        except Exception, e:
            print str(e)
            ret_dict = {"responseStr":"Del_failed"}
            json.dumps(ret_dict)
            return json_ret
