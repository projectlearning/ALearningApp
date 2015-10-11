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

class user:
    def __init__(self, AcademicQualification = 0, TotalNumOfClassInTimes = 0, AddressForClass = "", FirstName = "", TeacherCertifeVerification = 0, LastName = "", GraduateFrom = "", UserID = 0, UserType = 0, IDCardVerification = 0, ProfilePhotoURL = "", ExperienceInYears = 0, GraduationCertificateVerification = 0, UserProfileID = 0, TotalNumOfClassInHours = 0, OverallRate = 0.0, GoodRate = 0.0):
        self.AcademicQualification = AcademicQualification
        self.TotalNumOfClassInTimes = TotalNumOfClassInTimes
        self.AddressForClass = AddressForClass
        self.FirstName = FirstName
        self.TeacherCertifeVerification = TeacherCertifeVerification
        self.LastName = LastName
        self.GraduateFrom = GraduateFrom
        self.UserID = UserID
        self.UserType = UserType
        self.IDCardVerification = IDCardVerification
        self.ProfilePhotoURL = ProfilePhotoURL
        self.ExperienceInYears = ExperienceInYears
        self.GraduationCertificateVerification = GraduationCertificateVerification
        self.UserProfileID = UserProfileID
        self.TotalNumOfClassInHours = TotalNumOfClassInHours
        self.OverallRate = OverallRate
        self.GoodRate = GoodRate

class userprofile:
    def __init__(self, AcademicQualification = 0, TotalNumOfClassInTimes = 0, AddressForClass = "", FirstName = "", TeacherCertifeVerification = 0, LastName = "", GraduateFrom = "", UserID = 0, UserType = 0, IDCardVerification = 0, ProfilePhotoURL = "", ExperienceInYears = 0, GraduationCertificateVerification = 0, UserProfileID = 0, TotalNumOfClassInHours = 0, OverallRate = 0.0, GoodRate = 0.0):
        self.AcademicQualification = AcademicQualification
        self.TotalNumOfClassInTimes = TotalNumOfClassInTimes
        self.AddressForClass = AddressForClass
        self.FirstName = FirstName
        self.TeacherCertifeVerification = TeacherCertifeVerification
        self.LastName = LastName
        self.GraduateFrom = GraduateFrom
        self.UserID = UserID
        self.UserType = UserType
        self.IDCardVerification = IDCardVerification
        self.ProfilePhotoURL = ProfilePhotoURL
        self.ExperienceInYears = ExperienceInYears
        self.GraduationCertificateVerification = GraduationCertificateVerification
        self.UserProfileID = UserProfileID
        self.TotalNumOfClassInHours = TotalNumOfClassInHours
        self.OverallRate = OverallRate
        self.GoodRate = GoodRate
class teachingrecords:
    def __init__(self, EndTime = 0, TeachingRecordsID = 0, UserID = 0, Description = "", StartTime = 0):
        self.EndTime = EndTime
        self.TeachingRecordsID = TeachingRecordsID
        self.UserID = UserID
        self.Description = Description
        self.StartTime = StartTime

class successfulcases:
    def __init__(self, EndTime = 0, SuccessfulCasesID = 0, UserID = 0, Description = "", StartTime = 0):
        self.EndTime = EndTime
        self.SuccessfulCasesID = SuccessfulCasesID
        self.UserID = UserID
        self.Description = Description
        self.StartTime = StartTime

class verification:
    def __init__(self, VericationType = 0, VerificationID = 0, CodeNumber = "", UserID = 0, UploadImageWithFaceURL = "", UploadImageFrontURL = "", UploadImageBackURL = "", VerificationStatus = 0):
        self.VericationType = VericationType
        self.VerificationID = VerificationID
        self.CodeNumber = CodeNumber
        self.UserID = UserID
        self.UploadImageWithFaceURL = UploadImageWithFaceURL
        self.UploadImageFrontURL = UploadImageFrontURL
        self.UploadImageBackURL = UploadImageBackURL
        self.VerificationStatus = VerificationStatus
