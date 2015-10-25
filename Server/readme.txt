server start：
python alearning_server.py -p "port" [-i "configname"] [-d]
-p: port
-d: daemon
-i: configfile

database table:
{
    CREATE TABLE User
    (
         UserID                  BIGINT AUTO_INCREMENT,        -- unique, should be unsigned integer type(so the BIGINT is just for draft)
         PhoneNum                VARCHAR(20),   -- for user login, unique
         Password                VARCHAR(64),   -- length may need to be modified for encryption
         Username                VARCHAR(50),   -- NOT for user login, but for display to other users; e.g. Will Smith   
         Email                   VARCHAR(255),  -- user can also choose to register with email
         Token                   VARCHAR(255),  -- used to distinguish different user clients?
         FirstName               VARCHAR(50),    -- should be real and matches the IDCard
         LastName                VARCHAR(50),    -- should be real and matches the IDCard
         ProfilePhotoURL         VARCHAR(255),   -- URL of the profile photo
         UserType                TINYINT,        -- 0 - Parent, 1 - Certified Teacher, 2 - Uncertified Teacher, 3 - College Student, 4 - Institution
         ExperienceInYears       TINYINT,        -- how much experience does the teacher have in teaching; e.g. 5 years
         AcademicQualification   TINYINT,        -- 0 - Secondary School, 1 - Undergraduate(ongoing), 2 - Bachelor(certified), 3 - Graduate(master ongoing), 4 - Master(certified), 5 - Graduate(doctor ongoing), 6 - Doctor(certified)
         GraduateFrom            VARCHAR(255),   -- name of the institution from which the user graduates

         IDCardVerification                  TINYINT,    -- 0 - Not uploaded yet, 1 - Under verification, 2 - Verified, 3 - Fail to verify
         TeacherCertifeVerification          TINYINT,    -- 0 - Not uploaded yet, 1 - Under verification, 2 - Verified, 3 - Fail to verify
         GraduationCertificateVerification   TINYINT,    -- 0 - Not uploaded yet, 1 - Under verification, 2 - Verified, 3 - Fail to verify

         TotalNumOfClassInHours  INT,   -- the total number of hours that the teacher has spent teaching; e.g. 100 hours, for 50 times, 2 hour per time
         TotalNumOfClassInTimes  INT,   -- the total times that the teacher has had class; e.g. 50 times, for 100 hours, 2 hour per time

         OverallRate             DECIMAL, -- Good 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0 Bad; E.g. sum of all rate / sum of all votes, 20.0 / 5 = 4.0
         GoodRate                DECIMAL, -- >= rate 4 means Good, < 4 means not Good; E.g. number of good rate / total number of votes, 4 / 5 = 80%

         AddressForClass         VARCHAR(255),   -- To be confirmed what exactly it is for


         PRIMARY KEY (UserID)
    );

    CREATE TABLE teachingrecords
    (
         TeachingRecordsID   BIGINT,
         UserID              BIGINT,
         StartTime           INT,           -- e.g. 2010-09-01
         EndTime             INT,           -- e.g. 2015-07-30
         Description         VARCHAR(500),   -- e.g. Taught in xxx high school

         FOREIGN KEY (UserID) REFERENCES User(UserID),
         PRIMARY KEY (TeachingRecordsID)
    );

    CREATE TABLE successfulcases
    (
         SuccessfulCasesID   BIGINT,
         UserID              BIGINT,
         StartTime           INT,           -- e.g. 2014-09-01
         EndTime             INT,           -- e.g. 2015-02-01
         Description         VARCHAR(500),   -- e.g. Tutored a student called xxx, and has helped him improve his Math from grade C to grade D

         FOREIGN KEY (UserID) REFERENCES User(UserID),
         PRIMARY KEY (SuccessfulCasesID)
    );

    CREATE TABLE Verification
    (
         VerificationID          BIGINT,
         UserID                  BIGINT,
         VericationType          TINYINT,           -- 0 - IDCard, 1 - Teacher Certificate, 2 - Graduation Certificate
         CodeNumber              VARCHAR(255),   -- e.g. IDCard number, Certificate number, student card number
         VerificationStatus      TINYINT,        -- 0 - Not uploaded yet, 1 - Under verification, 2 - Verified, 3 - Fail to verify
         UploadImageFrontURL     VARCHAR(255),   -- image of front side of the item
         UploadImageBackURL      VARCHAR(255),   -- image of back side of the item
         UploadImageWithFaceURL  VARCHAR(255),   -- image of user holding the item(front side)

         FOREIGN KEY (UserID) REFERENCES User(UserID),
         PRIMARY KEY (VerificationID)
    );
}

