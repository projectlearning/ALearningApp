import MySQLdb
import sys
sys.path.append("../util")
from comm import *
import log

class AccountDao(object):
    def __init__(self, config):
        print "in accountdao"
        self.logger = log.loginit()
        self.__db = None try:
            self.__db = MySQLdb.connect(config.getIp(), config.getUser(), config.getPasswd(), config.getDbname()) self.__cursor = self.__db.cursor()
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
        Exception, e:
            return DB_GET_FAIL

    def add_clientaccount(self, st_clientaccount)
        sql = "Insert Into clientaccount(cid, token, passwd, deviceid, version, appversion, sesssionkey, sessiontime, createtime, lastlogintime) Values ('%d', '%s', '%s', '%s', '%s', '%d', '%s', '%d', '%d', '%d')" % (st_clientaccount.cid, st_clientaccount.token, st_clientaccount.passwd, st_clientaccount.deviceid, st_clientaccount.version, st_clientaccount.appversion, st_clientaccount.sesssionkey, st_clientaccount.sessiontime, st_clientaccount.createtime, st_clientaccount.lastlogintime)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_clientaccount(self, st_clientaccount)
        sql = "Update clientaccount Set cid = '%d', token = '%s', passwd = '%s', deviceid = '%s', version = '%s', appversion = '%d', sesssionkey = '%s', sessiontime = '%d', createtime = '%d', lastlogintime = '%d')Where cid = '%d'" % (st_clientaccount.cid, st_clientaccount.token, st_clientaccount.passwd, st_clientaccount.deviceid, st_clientaccount.version, st_clientaccount.appversion, st_clientaccount.sesssionkey, st_clientaccount.sessiontime, st_clientaccount.createtime, st_clientaccount.lastlogintime)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_clientaccount(self, st_clientaccount)
        sql = "Delete From clientaccount where cid = '%d'" % (cid)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL

    def get_user(self, UserID):
        
        sql = "Select * from account where UserID = '%ld'" % (UserID)
        try:
            self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        for row in results:
                UserID = row[0]
                PhoneNum = row[1]
                Password = row[2]
                Username = row[3]
                Email = row[4]
                Token = row[5]
                user = st_user(UserID, PhoneNum, Password, Username, Email, Token)
            return DB_OK, st_user
        Exception, e:
            return DB_GET_FAIL
    def get_user(self, UserProfileID):
        
        sql = "Select * from account where UserProfileID = '%ld'" % (UserProfileID)
        try:
            self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        for row in results:
                UserID = row[0]
                UserProfileID = row[1]
                FirstName = row[2]
                LastName = row[3]
                ProfilePhotoURL = row[4]
                UserType = row[5]
                ExperienceInYears = row[6]
                AcademicQualification = row[7]
                GraduateFrom = row[8]
                IDCardVerification = row[9]
                TeacherCertifeVerification = row[10]
                GraduationCertificateVerification = row[11]
                TotalNumOfClassInHours = row[12]
                TotalNumOfClassInTimes = row[13]
                OverallRate = row[14]
                GoodRate = row[15]
                AddressForClass = row[16]
                user = st_user(UserID, UserProfileID, FirstName, LastName, ProfilePhotoURL, UserType, ExperienceInYears, AcademicQualification, GraduateFrom, IDCardVerification, TeacherCertifeVerification, GraduationCertificateVerification, TotalNumOfClassInHours, TotalNumOfClassInTimes, OverallRate, GoodRate, AddressForClass)
            return DB_OK, st_user
        Exception, e:
            return DB_GET_FAIL

    def add_user(self, st_user)
        sql = "Insert Into user(UserID, UserProfileID, FirstName, LastName, ProfilePhotoURL, UserType, ExperienceInYears, AcademicQualification, GraduateFrom, IDCardVerification, TeacherCertifeVerification, GraduationCertificateVerification, TotalNumOfClassInHours, TotalNumOfClassInTimes, OverallRate, GoodRate, AddressForClass) Values ('%ld', '%ld', '%s', '%s', '%s', '%d', '%d', '%d', '%s', '%d', '%d', '%d', '%d', '%d', '%lf', '%lf', '%s')" % (st_user.UserID, st_user.UserProfileID, st_user.FirstName, st_user.LastName, st_user.ProfilePhotoURL, st_user.UserType, st_user.ExperienceInYears, st_user.AcademicQualification, st_user.GraduateFrom, st_user.IDCardVerification, st_user.TeacherCertifeVerification, st_user.GraduationCertificateVerification, st_user.TotalNumOfClassInHours, st_user.TotalNumOfClassInTimes, st_user.OverallRate, st_user.GoodRate, st_user.AddressForClass)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_user(self, st_user)
        sql = "Update user Set UserID = '%ld', UserProfileID = '%ld', FirstName = '%s', LastName = '%s', ProfilePhotoURL = '%s', UserType = '%d', ExperienceInYears = '%d', AcademicQualification = '%d', GraduateFrom = '%s', IDCardVerification = '%d', TeacherCertifeVerification = '%d', GraduationCertificateVerification = '%d', TotalNumOfClassInHours = '%d', TotalNumOfClassInTimes = '%d', OverallRate = '%lf', GoodRate = '%lf', AddressForClass = '%s')Where UserProfileID = '%ld'" % (st_user.UserID, st_user.UserProfileID, st_user.FirstName, st_user.LastName, st_user.ProfilePhotoURL, st_user.UserType, st_user.ExperienceInYears, st_user.AcademicQualification, st_user.GraduateFrom, st_user.IDCardVerification, st_user.TeacherCertifeVerification, st_user.GraduationCertificateVerification, st_user.TotalNumOfClassInHours, st_user.TotalNumOfClassInTimes, st_user.OverallRate, st_user.GoodRate, st_user.AddressForClass)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_user(self, st_user)
        sql = "Delete From user where UserProfileID = '%ld'" % (UserProfileID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL
    def get_userprofile(self, UserProfileID):
        
        sql = "Select * from account where UserProfileID = '%ld'" % (UserProfileID)
        try:
            self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        for row in results:
                UserID = row[0]
                UserProfileID = row[1]
                FirstName = row[2]
                LastName = row[3]
                ProfilePhotoURL = row[4]
                UserType = row[5]
                ExperienceInYears = row[6]
                AcademicQualification = row[7]
                GraduateFrom = row[8]
                IDCardVerification = row[9]
                TeacherCertifeVerification = row[10]
                GraduationCertificateVerification = row[11]
                TotalNumOfClassInHours = row[12]
                TotalNumOfClassInTimes = row[13]
                OverallRate = row[14]
                GoodRate = row[15]
                AddressForClass = row[16]
                userprofile = st_userprofile(UserID, UserProfileID, FirstName, LastName, ProfilePhotoURL, UserType, ExperienceInYears, AcademicQualification, GraduateFrom, IDCardVerification, TeacherCertifeVerification, GraduationCertificateVerification, TotalNumOfClassInHours, TotalNumOfClassInTimes, OverallRate, GoodRate, AddressForClass)
            return DB_OK, st_userprofile
        Exception, e:
            return DB_GET_FAIL

    def add_userprofile(self, st_userprofile)
        sql = "Insert Into userprofile(UserID, UserProfileID, FirstName, LastName, ProfilePhotoURL, UserType, ExperienceInYears, AcademicQualification, GraduateFrom, IDCardVerification, TeacherCertifeVerification, GraduationCertificateVerification, TotalNumOfClassInHours, TotalNumOfClassInTimes, OverallRate, GoodRate, AddressForClass) Values ('%ld', '%ld', '%s', '%s', '%s', '%d', '%d', '%d', '%s', '%d', '%d', '%d', '%d', '%d', '%lf', '%lf', '%s')" % (st_userprofile.UserID, st_userprofile.UserProfileID, st_userprofile.FirstName, st_userprofile.LastName, st_userprofile.ProfilePhotoURL, st_userprofile.UserType, st_userprofile.ExperienceInYears, st_userprofile.AcademicQualification, st_userprofile.GraduateFrom, st_userprofile.IDCardVerification, st_userprofile.TeacherCertifeVerification, st_userprofile.GraduationCertificateVerification, st_userprofile.TotalNumOfClassInHours, st_userprofile.TotalNumOfClassInTimes, st_userprofile.OverallRate, st_userprofile.GoodRate, st_userprofile.AddressForClass)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_userprofile(self, st_userprofile)
        sql = "Update userprofile Set UserID = '%ld', UserProfileID = '%ld', FirstName = '%s', LastName = '%s', ProfilePhotoURL = '%s', UserType = '%d', ExperienceInYears = '%d', AcademicQualification = '%d', GraduateFrom = '%s', IDCardVerification = '%d', TeacherCertifeVerification = '%d', GraduationCertificateVerification = '%d', TotalNumOfClassInHours = '%d', TotalNumOfClassInTimes = '%d', OverallRate = '%lf', GoodRate = '%lf', AddressForClass = '%s')Where UserProfileID = '%ld'" % (st_userprofile.UserID, st_userprofile.UserProfileID, st_userprofile.FirstName, st_userprofile.LastName, st_userprofile.ProfilePhotoURL, st_userprofile.UserType, st_userprofile.ExperienceInYears, st_userprofile.AcademicQualification, st_userprofile.GraduateFrom, st_userprofile.IDCardVerification, st_userprofile.TeacherCertifeVerification, st_userprofile.GraduationCertificateVerification, st_userprofile.TotalNumOfClassInHours, st_userprofile.TotalNumOfClassInTimes, st_userprofile.OverallRate, st_userprofile.GoodRate, st_userprofile.AddressForClass)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_userprofile(self, st_userprofile)
        sql = "Delete From userprofile where UserProfileID = '%ld'" % (UserProfileID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL
    def get_teachingrecords(self, TeachingRecordsID):
        
        sql = "Select * from account where TeachingRecordsID = '%ld'" % (TeachingRecordsID)
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
        Exception, e:
            return DB_GET_FAIL

    def add_teachingrecords(self, st_teachingrecords)
        sql = "Insert Into teachingrecords(TeachingRecordsID, UserID, StartTime, EndTime, Description) Values ('%ld', '%ld', '%d', '%d', '%s')" % (st_teachingrecords.TeachingRecordsID, st_teachingrecords.UserID, st_teachingrecords.StartTime, st_teachingrecords.EndTime, st_teachingrecords.Description)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_teachingrecords(self, st_teachingrecords)
        sql = "Update teachingrecords Set TeachingRecordsID = '%ld', UserID = '%ld', StartTime = '%d', EndTime = '%d', Description = '%s')Where TeachingRecordsID = '%ld'" % (st_teachingrecords.TeachingRecordsID, st_teachingrecords.UserID, st_teachingrecords.StartTime, st_teachingrecords.EndTime, st_teachingrecords.Description)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_teachingrecords(self, st_teachingrecords)
        sql = "Delete From teachingrecords where TeachingRecordsID = '%ld'" % (TeachingRecordsID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL
    def get_successfulcases(self, SuccessfulCasesID):
        
        sql = "Select * from account where SuccessfulCasesID = '%ld'" % (SuccessfulCasesID)
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
        Exception, e:
            return DB_GET_FAIL

    def add_successfulcases(self, st_successfulcases)
        sql = "Insert Into successfulcases(SuccessfulCasesID, UserID, StartTime, EndTime, Description) Values ('%ld', '%ld', '%d', '%d', '%s')" % (st_successfulcases.SuccessfulCasesID, st_successfulcases.UserID, st_successfulcases.StartTime, st_successfulcases.EndTime, st_successfulcases.Description)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_successfulcases(self, st_successfulcases)
        sql = "Update successfulcases Set SuccessfulCasesID = '%ld', UserID = '%ld', StartTime = '%d', EndTime = '%d', Description = '%s')Where SuccessfulCasesID = '%ld'" % (st_successfulcases.SuccessfulCasesID, st_successfulcases.UserID, st_successfulcases.StartTime, st_successfulcases.EndTime, st_successfulcases.Description)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_successfulcases(self, st_successfulcases)
        sql = "Delete From successfulcases where SuccessfulCasesID = '%ld'" % (SuccessfulCasesID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL
    def get_verification(self, VerificationID):
        
        sql = "Select * from account where VerificationID = '%ld'" % (VerificationID)
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
        Exception, e:
            return DB_GET_FAIL

    def add_verification(self, st_verification)
        sql = "Insert Into verification(VerificationID, UserID, VericationType, CodeNumber, VerificationStatus, UploadImageFrontURL, UploadImageBackURL, UploadImageWithFaceURL) Values ('%ld', '%ld', '%d', '%s', '%d', '%s', '%s', '%s')" % (st_verification.VerificationID, st_verification.UserID, st_verification.VericationType, st_verification.CodeNumber, st_verification.VerificationStatus, st_verification.UploadImageFrontURL, st_verification.UploadImageBackURL, st_verification.UploadImageWithFaceURL)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_ADD_FAIL

    def update_verification(self, st_verification)
        sql = "Update verification Set VerificationID = '%ld', UserID = '%ld', VericationType = '%d', CodeNumber = '%s', VerificationStatus = '%d', UploadImageFrontURL = '%s', UploadImageBackURL = '%s', UploadImageWithFaceURL = '%s')Where VerificationID = '%ld'" % (st_verification.VerificationID, st_verification.UserID, st_verification.VericationType, st_verification.CodeNumber, st_verification.VerificationStatus, st_verification.UploadImageFrontURL, st_verification.UploadImageBackURL, st_verification.UploadImageWithFaceURL)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_UPDATE_FAIL

    def del_verification(self, st_verification)
        sql = "Delete From verification where VerificationID = '%ld'" % (VerificationID)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return DB_OK
        except Exception, e:
            self.__db.rollback()
        return DB_DEL_FAIL
