    def get_clientaccount(self, cid):
        
        "Select * from account where cid = '%d'" % (cid)
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
