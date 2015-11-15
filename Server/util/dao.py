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

    def get_clientaccount(self, cid):
        
        sql = "Select * from account where cid = '%d'" % (cid)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            for row in results:
                cid = row[0]
                token = row[1]
                passwd = row[2]
                deviceid = row[3]
                version = row[4]
                appversion = row[5]
                sesssionkey = row[6]
                sessiontime = row[7]
                createtime = row[8]
                lastlogintime = row[9]
                clientaccount = st_clientaccount(cid, token, passwd, deviceid, version, appversion, sesssionkey, sessiontime, createtime, lastlogintime)
            return DB_OK, st_clientaccount
        except Exception, e:
            return DB_GET_FAIL

    def add_clientaccount(self, st_clientaccount):
        sql = "Insert Into clientaccount(cid, token, passwd, deviceid, version, appversion, sesssionkey, sessiontime, createtime, lastlogintime) Values ('%d', '%s', '%s', '%s', '%s', '%d', '%s', '%d', '%d', '%d')" % (st_clientaccount.cid, st_clientaccount.token, st_clientaccount.passwd, st_clientaccount.deviceid, st_clientaccount.version, st_clientaccount.appversion, st_clientaccount.sesssionkey, st_clientaccount.sessiontime, st_clientaccount.createtime, st_clientaccount.lastlogintime)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_clientaccount(self, st_clientaccount):
        sql = "Update clientaccount Set cid = '%d', token = '%s', passwd = '%s', deviceid = '%s', version = '%s', appversion = '%d', sesssionkey = '%s', sessiontime = '%d', createtime = '%d', lastlogintime = '%d' Where cid = '%d'" % (st_clientaccount.cid, st_clientaccount.token, st_clientaccount.passwd, st_clientaccount.deviceid, st_clientaccount.version, st_clientaccount.appversion, st_clientaccount.sesssionkey, st_clientaccount.sessiontime, st_clientaccount.createtime, st_clientaccount.lastlogintime)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_clientaccount(self, st_clientaccount):
        sql = "Delete From clientaccount where cid = '%d'" % (cid)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_teachingrecords(self, TeachingRecordsID):
        
        sql = "Select * from teachingrecords where TeachingRecordsID = '%ld'" % (TeachingRecordsID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            for row in results:
                TeachingRecordsID = row[0]
                UserID = row[1]
                StartTime = row[2]
                EndTime = row[3]
                Description = row[4]
                teachingrecords = st_teachingrecords(TeachingRecordsID, UserID, StartTime, EndTime, Description)
            return DB_OK, st_teachingrecords
        except Exception, e:
            return DB_GET_FAIL, None

    def add_teachingrecords(self, st_teachingrecords):
        sql = "Insert Into teachingrecords(TeachingRecordsID, UserID, StartTime, EndTime, Description) Values ('%ld', '%ld', '%d', '%d', '%s')" % (st_teachingrecords.TeachingRecordsID, st_teachingrecords.UserID, st_teachingrecords.StartTime, st_teachingrecords.EndTime, st_teachingrecords.Description)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_teachingrecords(self, st_teachingrecords):
        sql = "Update teachingrecords Set TeachingRecordsID = '%ld', UserID = '%ld', StartTime = '%d', EndTime = '%d', Description = '%s' where TeachingRecordsID = '%ld'" % (st_teachingrecords.TeachingRecordsID, st_teachingrecords.UserID, st_teachingrecords.StartTime, st_teachingrecords.EndTime, st_teachingrecords.Description, st_teachingrecords.TeachingRecordsID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_teachingrecords(self, st_teachingrecords):
        sql = "Delete From teachingrecords where TeachingRecordsID = '%ld'" % (TeachingRecordsID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL
    def get_successfulcases(self, SuccessfulCasesID):
        
        sql = "Select * from successfulcases where SuccessfulCasesID = '%ld'" % (SuccessfulCasesID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            for row in results:
                SuccessfulCasesID = row[0]
                UserID = row[1]
                StartTime = row[2]
                EndTime = row[3]
                Description = row[4]
                successfulcases = st_successfulcases(SuccessfulCasesID, UserID, StartTime, EndTime, Description)
            return DB_OK, st_successfulcases
        except Exception, e:
            return DB_GET_FAIL

    def add_successfulcases(self, st_successfulcases):
        sql = "Insert Into successfulcases(SuccessfulCasesID, UserID, StartTime, EndTime, Description) Values ('%ld', '%ld', '%d', '%d', '%s')" % (st_successfulcases.SuccessfulCasesID, st_successfulcases.UserID, st_successfulcases.StartTime, st_successfulcases.EndTime, st_successfulcases.Description)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_successfulcases(self, st_successfulcases):
        sql = "Update successfulcases Set SuccessfulCasesID = '%ld', UserID = '%ld', StartTime = '%d', EndTime = '%d', Description = '%s' where SuccessfulCasesID = '%ld'" % (st_successfulcases.SuccessfulCasesID, st_successfulcases.UserID, st_successfulcases.StartTime, st_successfulcases.EndTime, st_successfulcases.Description, st_successfulcases.SuccessfulCasesID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_successfulcases(self, st_successfulcases):
        sql = "Delete From successfulcases where SuccessfulCasesID = '%ld'" % (SuccessfulCasesID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL
    def get_verification(self, VerificationID):
        
        sql = "Select * from verification where VerificationID = '%ld'" % (VerificationID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            for row in results:
                VerificationID = row[0]
                UserID = row[1]
                VericationType = row[2]
                CodeNumber = row[3]
                VerificationStatus = row[4]
                UploadImageFrontURL = row[5]
                UploadImageBackURL = row[6]
                UploadImageWithFaceURL = row[7]
                verification = st_verification(VerificationID, UserID, VericationType, CodeNumber, VerificationStatus, UploadImageFrontURL, UploadImageBackURL, UploadImageWithFaceURL)
            return DB_OK, st_verification
        except Exception, e:
            return DB_GET_FAIL

    def add_verification(self, st_verification):
        sql = "Insert Into verification(VerificationID, UserID, VericationType, CodeNumber, VerificationStatus, UploadImageFrontURL, UploadImageBackURL, UploadImageWithFaceURL) Values ('%ld', '%ld', '%d', '%s', '%d', '%s', '%s', '%s')" % (st_verification.VerificationID, st_verification.UserID, st_verification.VericationType, st_verification.CodeNumber, st_verification.VerificationStatus, st_verification.UploadImageFrontURL, st_verification.UploadImageBackURL, st_verification.UploadImageWithFaceURL)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_verification(self, st_verification):
        sql = "Update verification Set VerificationID = '%ld', UserID = '%ld', VericationType = '%d', CodeNumber = '%s', VerificationStatus = '%d', UploadImageFrontURL = '%s', UploadImageBackURL = '%s', UploadImageWithFaceURL = '%s' where VerificationID = '%ld'" % (st_verification.VerificationID, st_verification.UserID, st_verification.VericationType, st_verification.CodeNumber, st_verification.VerificationStatus, st_verification.UploadImageFrontURL, st_verification.UploadImageBackURL, st_verification.UploadImageWithFaceURL, st_verification.VerificationID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_verification(self, st_verification):
        sql = "Delete From verification where VerificationID = '%ld'" % (VerificationID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_user_by_userid(self, UserID):
        sql = "Select * from user where UserID = '%ld'" % (UserID)
        print sql
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            if len(results) <= 0:
                return DB_GET_FAIL, None
            row = results[0]
            UserID = row[0]
            PhoneNum = row[1]
            Password = row[2]
            Username = row[3]
            Email = row[4]
            Token = row[5]
            FirstName = row[6]
            LastName = row[7]
            ProfilePhotoURL = row[8]
            UserType = row[9]
            AcademicQualification = row[10]
            ExperienceInYears = row[11]
            GraduateFrom = row[12]
            IDCardVerification = row[13]
            TeacherCertifeVerification = row[14]
            GraduationCertificateVerification = row[15]
            TotalNumOfClassInHours = row[16]
            TotalNumOfClassInTimes = row[17]
            OverallRate = row[18]
            GoodRate = row[19]
            AddressForClass = row[20]
            st_user = user(UserID, PhoneNum, Password, Username, Email, Token, FirstName, LastName, ProfilePhotoURL, UserType, AcademicQualification, ExperienceInYears, GraduateFrom, IDCardVerification, TeacherCertifeVerification, GraduationCertificateVerification, TotalNumOfClassInHours, TotalNumOfClassInTimes, OverallRate, GoodRate, AddressForClass)
            return DB_OK, st_user
        except Exception, e:
            return DB_GET_FAIL, None

    def get_user_by_phonenum(self, PhoneNum):
        sql = "Select * from user where PhoneNum = '%s'" % (PhoneNum)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            if len(results) <= 0:
                return DB_GET_FAIL, None
            row = results[0]
            UserID = row[0]
            PhoneNum = row[1]
            Password = row[2]
            Username = row[3]
            Email = row[4]
            Token = row[5]
            FirstName = row[6]
            LastName = row[7]
            ProfilePhotoURL = row[8]
            UserType = row[9]
            AcademicQualification = row[10]
            ExperienceInYears = row[11]
            GraduateFrom = row[12]
            IDCardVerification = row[13]
            TeacherCertifeVerification = row[14]
            GraduationCertificateVerification = row[15]
            TotalNumOfClassInHours = row[16]
            TotalNumOfClassInTimes = row[17]
            OverallRate = row[18]
            GoodRate = row[19]
            AddressForClass = row[20]
            st_user = user(UserID, PhoneNum, Password, Username, Email, Token, FirstName, LastName, ProfilePhotoURL, UserType, AcademicQualification, ExperienceInYears, GraduateFrom, IDCardVerification, TeacherCertifeVerification, GraduationCertificateVerification, TotalNumOfClassInHours, TotalNumOfClassInTimes, OverallRate, GoodRate, AddressForClass)
            print st_user.UserID
            return DB_OK, st_user
        except Exception, e:
            print str(e)
            return DB_GET_FAIL, None


    def add_user(self, st_user):
        sql = "Insert Into user(UserID, PhoneNum, Password, Username, Email, Token, FirstName, LastName, ProfilePhotoURL, UserType, AcademicQualification, ExperienceInYears, GraduateFrom, IDCardVerification, TeacherCertifeVerification, GraduationCertificateVerification, TotalNumOfClassInHours, TotalNumOfClassInTimes, OverallRate, GoodRate, AddressForClass) Values ('%ld', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%d', '%s', '%d', '%d', '%d', '%d', '%d', '%lf', '%lf', '%s')" % (st_user.UserID, st_user.PhoneNum, st_user.Password, st_user.Username, st_user.Email, st_user.Token, st_user.FirstName, st_user.LastName, st_user.ProfilePhotoURL, st_user.UserType, st_user.AcademicQualification, st_user.ExperienceInYears, st_user.GraduateFrom, st_user.IDCardVerification, st_user.TeacherCertifeVerification, st_user.GraduationCertificateVerification, st_user.TotalNumOfClassInHours, st_user.TotalNumOfClassInTimes, st_user.OverallRate, st_user.GoodRate, st_user.AddressForClass)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()

            query="SELECT LAST_INSERT_ID()";
            self.__cursor.execute(query)
            results = self.__cursor.fetchall()
            if len(results) <= 0:
                self.__db.rollback()
                return DB_ADD_FAIL

            row = results[0]
            st_user.UserID = long(row[0])
            print row[0]

            return DB_OK
        except Exception, e:
            self.__db.rollback()
            print str(e)
        return DB_ADD_FAIL

    def update_user(self, st_user):
        sql = "Update user Set UserID = '%ld', PhoneNum = '%s', Password = '%s', Username = '%s', Email = '%s', Token = '%s', FirstName = '%s', LastName = '%s', ProfilePhotoURL = '%s', UserType = '%d', AcademicQualification = '%d', ExperienceInYears = '%d', GraduateFrom = '%s', IDCardVerification = '%d', TeacherCertifeVerification = '%d', GraduationCertificateVerification = '%d', TotalNumOfClassInHours = '%d', TotalNumOfClassInTimes = '%d', OverallRate = '%lf', GoodRate = '%lf', AddressForClass = '%s' Where UserID = '%ld'" % (st_user.UserID, st_user.PhoneNum, st_user.Password, st_user.Username, st_user.Email, st_user.Token, st_user.FirstName, st_user.LastName, st_user.ProfilePhotoURL, st_user.UserType, st_user.AcademicQualification, st_user.ExperienceInYears, st_user.GraduateFrom, st_user.IDCardVerification, st_user.TeacherCertifeVerification, st_user.GraduationCertificateVerification, st_user.TotalNumOfClassInHours, st_user.TotalNumOfClassInTimes, st_user.OverallRate, st_user.GoodRate, st_user.AddressForClass, st_user.UserID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            print str(e)
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_user(self, st_user):
        sql = "Delete From user where UserID = '%ld'" % (UserID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_requirement(self, RequirementID):
        sql = "Select * from account where RequirementID = '%ld'" % (RequirementID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            
            if len(results) <= 0:
                return DB_GET_FAIL, None
            row = results[0]
            RequirementID = row[0]
            UserID = row[1]
            RequirementType = row[2]
            MaxPrice = row[3]
            MinPrice = row[4]
            Mode = row[5]
            Status = row[6]
            PostDate = row[7]
            st_requirement = requirement(RequirementID, UserID, RequirementType, MaxPrice, MinPrice, Mode, Status, PostDate)
            return DB_OK, st_requirement
        except Exception, e:
            return DB_GET_FAIL, None

    def add_requirement(self, st_requirement):
        sql = "Insert Into requirement(RequirementID, UserID, RequirementType, MaxPrice, MinPrice, Mode, Status, PostDate) Values ('%ld', '%ld', '%d', '%d', '%d', '%d', '%d', '%d')" % (st_requirement.RequirementID, st_requirement.UserID, st_requirement.RequirementType, st_requirement.MaxPrice, st_requirement.MinPrice, st_requirement.Mode, st_requirement.Status, st_requirement.PostDate)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_requirement(self, st_requirement):
        sql = "Update requirement Set RequirementID = '%ld', UserID = '%ld', RequirementType = '%d', MaxPrice = '%d', MinPrice = '%d', Mode = '%d', Status = '%d', PostDate = '%d' Where RequirementID = '%ld'" % (st_requirement.RequirementID, st_requirement.UserID, st_requirement.RequirementType, st_requirement.MaxPrice, st_requirement.MinPrice, st_requirement.Mode, st_requirement.Status, st_requirement.PostDate, st_requirement.RequirementID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_requirement(self, st_requirement):
        sql = "Delete From requirement where RequirementID = '%ld'" % (RequirementID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_requirementtime(self, ID):
        sql = "Select * from account where ID = '%ld'" % (ID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            
            if len(results) <= 0:
                return DB_GET_FAIL, None
            row = results[0]
            ID = row[0]
            RequirementID = row[1]
            Date = row[2]
            Period = row[3]
            IsActive = row[4]
            st_requirementtime = requirementtime(ID, RequirementID, Date, Period, IsActive)
            return DB_OK, st_requirementtime
        except Exception, e:
            return DB_GET_FAIL, None

    def add_requirementtime(self, st_requirementtime):
        sql = "Insert Into requirementtime(ID, RequirementID, Date, Period, IsActive) Values ('%ld', '%ld', '%d', '%d', '%d')" % (st_requirementtime.ID, st_requirementtime.RequirementID, st_requirementtime.Date, st_requirementtime.Period, st_requirementtime.IsActive)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_requirementtime(self, st_requirementtime):
        sql = "Update requirementtime Set ID = '%ld', RequirementID = '%ld', Date = '%d', Period = '%d', IsActive = '%d' Where ID = '%ld'" % (st_requirementtime.ID, st_requirementtime.RequirementID, st_requirementtime.Date, st_requirementtime.Period, st_requirementtime.IsActive, st_requirementtime.ID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_requirementtime(self, st_requirementtime):
        sql = "Delete From requirementtime where ID = '%ld'" % (ID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_course(self, CourseID):
        sql = "Select * from account where CourseID = '%ld'" % (CourseID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            
            if len(results) <= 0:
                return DB_GET_FAIL, None
            row = results[0]
            CourseID = row[0]
            Grade = row[1]
            Name = row[2]
            st_course = course(CourseID, Grade, Name)
            return DB_OK, st_course
        except Exception, e:
            return DB_GET_FAIL, None

    def add_course(self, st_course):
        sql = "Insert Into course(CourseID, Grade, Name) Values ('%ld', '%d', '%s')" % (st_course.CourseID, st_course.Grade, st_course.Name)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_course(self, st_course):
        sql = "Update course Set CourseID = '%ld', Grade = '%d', Name = '%s' Where CourseID = '%ld'" % (st_course.CourseID, st_course.Grade, st_course.Name, st_course.CourseID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_course(self, st_course):
        sql = "Delete From course where CourseID = '%ld'" % (CourseID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_requirementcourse(self, ID):
        sql = "Select * from account where ID = '%ld'" % (ID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            
            if len(results) <= 0:
                return DB_GET_FAIL, None
            row = results[0]
            ID = row[0]
            RequirementID = row[1]
            CourseID = row[2]
            st_requirementcourse = requirementcourse(ID, RequirementID, CourseID)
            return DB_OK, st_requirementcourse
        except Exception, e:
            return DB_GET_FAIL, None

    def add_requirementcourse(self, st_requirementcourse):
        sql = "Insert Into requirementcourse(ID, RequirementID, CourseID) Values ('%ld', '%ld', '%ld')" % (st_requirementcourse.ID, st_requirementcourse.RequirementID, st_requirementcourse.CourseID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_requirementcourse(self, st_requirementcourse):
        sql = "Update requirementcourse Set ID = '%ld', RequirementID = '%ld', CourseID = '%ld' Where ID = '%ld'" % (st_requirementcourse.ID, st_requirementcourse.RequirementID, st_requirementcourse.CourseID, st_requirementcourse.ID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_requirementcourse(self, st_requirementcourse):
        sql = "Delete From requirementcourse where ID = '%ld'" % (ID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_addressconfig(self, AddressConfigID):
        sql = "Select * from account where AddressConfigID = '%ld'" % (AddressConfigID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            
            if len(results) <= 0:
                return DB_GET_FAIL, None
            row = results[0]
            AddressConfigID = row[0]
            Country = row[1]
            Province = row[2]
            City = row[3]
            District = row[4]
            st_addressconfig = addressconfig(AddressConfigID, Country, Province, City, District)
            return DB_OK, st_addressconfig
        except Exception, e:
            return DB_GET_FAIL, None

    def add_addressconfig(self, st_addressconfig):
        sql = "Insert Into addressconfig(AddressConfigID, Country, Province, City, District) Values ('%ld', '%s', '%s', '%s', '%s')" % (st_addressconfig.AddressConfigID, st_addressconfig.Country, st_addressconfig.Province, st_addressconfig.City, st_addressconfig.District)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_addressconfig(self, st_addressconfig):
        sql = "Update addressconfig Set AddressConfigID = '%ld', Country = '%s', Province = '%s', City = '%s', District = '%s' Where AddressConfigID = '%ld'" % (st_addressconfig.AddressConfigID, st_addressconfig.Country, st_addressconfig.Province, st_addressconfig.City, st_addressconfig.District, st_addressconfig.AddressConfigID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_addressconfig(self, st_addressconfig):
        sql = "Delete From addressconfig where AddressConfigID = '%ld'" % (AddressConfigID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_address(self, ID):
        sql = "Select * from account where ID = '%ld'" % (ID)
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            
            if len(results) <= 0:
                return DB_GET_FAIL, None
            row = results[0]
            ID = row[0]
            RequirementID = row[1]
            UserID = row[2]
            AddressConfigID = row[3]
            RestAddress = row[4]
            st_address = address(ID, RequirementID, UserID, AddressConfigID, RestAddress)
            return DB_OK, st_address
        except Exception, e:
            return DB_GET_FAIL, None

    def add_address(self, st_address):
        sql = "Insert Into address(ID, RequirementID, UserID, AddressConfigID, RestAddress) Values ('%ld', '%ld', '%ld', '%ld', '%s')" % (st_address.ID, st_address.RequirementID, st_address.UserID, st_address.AddressConfigID, st_address.RestAddress)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_address(self, st_address):
        sql = "Update address Set ID = '%ld', RequirementID = '%ld', UserID = '%ld', AddressConfigID = '%ld', RestAddress = '%s' Where ID = '%ld'" % (st_address.ID, st_address.RequirementID, st_address.UserID, st_address.AddressConfigID, st_address.RestAddress, st_address.ID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_address(self, st_address):
        sql = "Delete From address where ID = '%ld'" % (ID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL
