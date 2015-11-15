server start：
python alearning_server.py -p "port" [-i "configname"] [-d]
-p: port
-d: daemon
-i: configfile

database table:
{
    CREATE TABLE user
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
         UNIQUE KEY (PhoneNum)
    );
    ---- user_register, user_login, user_get, user_update

    CREATE TABLE teachingrecords
    (
         TeachingRecordsID   BIGINT AUTO_INCREMENT,
         UserID              BIGINT,
         StartTime           INT,           -- e.g. 2010-09-01
         EndTime             INT,           -- e.g. 2015-07-30
         Description         VARCHAR(500),   -- e.g. Taught in xxx high school

         FOREIGN KEY (UserID) REFERENCES user(UserID),
         PRIMARY KEY (TeachingRecordsID)
    );

    CREATE TABLE successfulcases
    (
         SuccessfulCasesID   BIGINT AUTO_INCREMENT,
         UserID              BIGINT,
         StartTime           INT,           -- e.g. 2014-09-01
         EndTime             INT,           -- e.g. 2015-02-01
         Description         VARCHAR(500),   -- e.g. Tutored a student called xxx, and has helped him improve his Math from grade C to grade D

         FOREIGN KEY (UserID) REFERENCES user(UserID),
         PRIMARY KEY (SuccessfulCasesID)
    );

    CREATE TABLE Verification
    (
         VerificationID          BIGINT AUTO_INCREMENT,
         UserID                  BIGINT,
         VericationType          TINYINT,           -- 0 - IDCard, 1 - Teacher Certificate, 2 - Graduation Certificate
         CodeNumber              VARCHAR(255),   -- e.g. IDCard number, Certificate number, student card number
         VerificationStatus      TINYINT,        -- 0 - Not uploaded yet, 1 - Under verification, 2 - Verified, 3 - Fail to verify
         UploadImageFrontURL     VARCHAR(255),   -- image of front side of the item
         UploadImageBackURL      VARCHAR(255),   -- image of back side of the item
         UploadImageWithFaceURL  VARCHAR(255),   -- image of user holding the item(front side)

         FOREIGN KEY (UserID) REFERENCES user(UserID),
         PRIMARY KEY (VerificationID)
    )CHARSET=utf8;

    CREATE TABLE requirement
    ( 
        RequirementID       BIGINT AUTO_INCREMENT,      -- unique, should be unsigned integer type(so the BIGINT is just for draft)
        UserID              BIGINT not NULL,
        RequirementType     TINYINT,     -- 0为找老师，1为找学生
        MaxPrice            TINYINT,     -- 价格上限
        MinPrice            TINYINT,     -- 价格下限
        Mode                TINYINT,     -- 授课方式，0为老师上门，1为学生上门，2为双方协定地址，3以上都可
        Status              TINYINT,     -- 需求状态，0为此需求已失效，1为此需求有效，2为该需求部分被承接
        PostDate            INT,

        FOREIGN KEY (UserID) REFERENCES user(UserID),
        PRIMARY KEY (RequirementID)
    )CHARSET=utf8; 
    
    CREATE TABLE requirementcourse                  
    (
         ID  BIGINT AUTO_INCREMENT,        -- unique, should be unsigned integer type(so the BIGINT is just for draft)
         RequirementID   BIGINT not NULL,
         CourseID    BIGINT not NULL,

         FOREIGN KEY (RequirementID) REFERENCES requirement(RequirementID),
         FOREIGN KEY (CourseID) REFERENCES course(CourseID),
         PRIMARY KEY (id)
    )CHARSET=utf8; 

    CREATE TABLE course            
    (
        CourseID    BIGINT AUTO_INCREMENT,          -- unique, should be unsigned integer type(so the BIGINT is just for draft)
        Grade       TINYINT,            -- 0为学前教育，1为小学，2为中学，3为高中
        Name        VARCHAR(255),       -- 可以考虑使用枚举变量
        
        PRIMARY KEY (CourseID)
    )CHARSET=utf8; 
    
    CREATE TABLE requirementtime   
    (
         ID              BIGINT AUTO_INCREMENT,     -- unique, should be unsigned integer type(so the BIGINT is just for draft)
         RequirementID   BIGINT not NULL,
         Date            INT,
         Period          TINYINT,    -- 0为上午，1为下午，2为晚上
         IsActive        TINYINT,

         FOREIGN KEY (RequirementID) REFERENCES requirement(RequirementID),
         PRIMARY KEY (id)
    )CHARSET=utf8; 

    CREATE TABLE address
    (
         ID  BIGINT AUTO_INCREMENT,
         RequirementID   BIGINT,
         UserID  BIGINT,
         AddressConfigID BIGINT not NULL,
         RestAddress VARCHAR(255),

         FOREIGN KEY (RequirementID) REFERENCES requirement(RequirementID),
         FOREIGN KEY (UserID) REFERENCES user(UserID),
         FOREIGN KEY (AddressConfigID) REFERENCES addressconfig(AddressConfigID),
         PRIMARY KEY (id)
    )CHARSET=utf8; 

    CREATE TABLE addressconfig
    (
        AddressConfigID  BIGINT AUTO_INCREMENT, 
        Country VARCHAR(255),
        Province    VARCHAR(255),
        City    VARCHAR(255),
        District    VARCHAR(255),

        PRIMARY KEY (AddressConfigID)
    )CHARSET=utf8; 

    ---- tablename_(get, add, update, del)
}
