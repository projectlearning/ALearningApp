import sys

DB_OK = 0
DB_GET_FAIL = -10001
DB_ADD_FAIL = -10002
DB_UPDATE_FAIL = -10003
DB_DEL_FAIL = -10004

class account:
    def __init__(self, cid = 0, nickname = "", sex = "", age = 0):
        self.cid = cid
        self.nickname = nickname
        self.sex = sex
        self.age = age

class clientaccount:
    def __init__(self, sesssionkey = "", cid = 0, passwd = "", appversion = 0, token = "", version = "", sessiontime = 0, deviceid = "", lastlogintime = 0, createtime = 0):
        self.sesssionkey = sesssionkey
        self.cid = cid
        self.passwd = passwd
        self.appversion = appversion
        self.token = token
        self.version = version
        self.sessiontime = sessiontime
        self.deviceid = deviceid
        self.lastlogintime = lastlogintime
        self.createtime = createtime


class User:
    def __init__(self, UserID = 0, PhoneNum = "", Password = "", Username = "", Email = "", Token = "", FirstName = "", LastName = "", ProfilePhotoURL = "", UserType = 0, AcademicQualification = 0, ExperienceInYears = 0, GraduateFrom = "", IDCardVerification = 0, TeacherCertifeVerification = 0, GraduationCertificateVerification = 0, TotalNumOfClassInHours = 0, TotalNumOfClassInTimes = 0, OverallRate = 0.0, GoodRate = 0.0, AddressForClass = ""):
        self.UserID = UserID
        self.PhoneNum = PhoneNum
        self.Password = Password
        self.Username = Username
        self.Email = Email
        self.Token = Token
        self.FirstName = FirstName
        self.LastName = LastName
        self.ProfilePhotoURL = ProfilePhotoURL
        self.UserType = UserType
        self.AcademicQualification = AcademicQualification
        self.ExperienceInYears = ExperienceInYears
        self.GraduateFrom = GraduateFrom
        self.IDCardVerification = IDCardVerification
        self.TeacherCertifeVerification = TeacherCertifeVerification
        self.GraduationCertificateVerification = GraduationCertificateVerification
        self.TotalNumOfClassInHours = TotalNumOfClassInHours
        self.TotalNumOfClassInTimes = TotalNumOfClassInTimes
        self.OverallRate = OverallRate
        self.GoodRate = GoodRate
        self.AddressForClass = AddressForClass

class teachingrecords:
    def __init__(self, TeachingRecordsID = 0, UserID = 0, StartTime = 0, EndTime = 0, Description = ""):
        self.TeachingRecordsID = TeachingRecordsID
        self.UserID = UserID
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Description = Description
class successfulcases:
    def __init__(self, SuccessfulCasesID = 0, UserID = 0, StartTime = 0, EndTime = 0, Description = ""):
        self.SuccessfulCasesID = SuccessfulCasesID
        self.UserID = UserID
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Description = Description
class verification:
    def __init__(self, VerificationID = 0, UserID = 0, VericationType = 0, CodeNumber = "", VerificationStatus = 0, UploadImageFrontURL = "", UploadImageBackURL = "", UploadImageWithFaceURL = ""):
        self.VerificationID = VerificationID
        self.UserID = UserID
        self.VericationType = VericationType
        self.CodeNumber = CodeNumber
        self.VerificationStatus = VerificationStatus
        self.UploadImageFrontURL = UploadImageFrontURL
        self.UploadImageBackURL = UploadImageBackURL
        self.UploadImageWithFaceURL = UploadImageWithFaceURL
