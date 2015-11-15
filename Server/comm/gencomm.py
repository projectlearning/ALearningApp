import sys, re

def addtab(tab):
    ret = "\n"
    for i in xrange(tab):
        ret += "    " 
    return ret

def initFromType(dbtype): 
    if dbtype == "varchar":
        return "\"\""
    elif dbtype == "int" or dbtype == "bigint" or dbtype == "tinyint":
        return "0"
    elif dbtype == "decimal":
        return "0.0"
    else:
        print dbtype

def changeFromType(dbtype):
    if dbtype == "varchar":
        return "str"
    elif dbtype == "int":
        return "int"
    elif dbtype == "bigint":
        return "long"
    elif dbtype == "tinyint":
        return "int"
    elif dbtype == "decimal":
        return "float"

def formatFromType(dbtype):
    if dbtype == "varchar":
        return "%s"
    elif dbtype == "int"  or dbtype == "tinyint":
        return "%d"
    elif dbtype == "bigint":
        return "%ld"
    elif dbtype == "decimal":
        return "%lf"

def getDict(tablename):
    inhandle = open(tablename+".txt", "r")
    itemdict = dict()
    itemlist = []
    typelist = []
    prikey = ""
    for index, line in enumerate(inhandle.readlines()):
        items = line.strip().split(" ")
        if items[0] == "Field":
            continue
        pos = items[1].find('(')
        itemdict[items[0]] = items[1][0:pos] 
        itemlist.append(items[0])
        typelist.append(items[1])
        print str(items)
        if len(items) > 2 and items[2] == "PRI":
            prikey = items[0]
    return itemdict, itemlist, typelist, prikey
 
def genClass(itemdict, itemlist, tablename, commname):
    outhandle= open(commname+".py", "a+")
    outhandle.write("class %s:\n" % (tablename))
    member_str = "    def __init__(self"
   
    for index in xrange(len(itemlist)):
        member_str += ", %s = %s" % (itemlist[index], initFromType(itemdict[itemlist[index]]))
    member_str += "):"

    tab = 2
    for index in xrange(len(itemlist)):
        member_str += addtab(2) + "self.%s = %s" % (itemlist[index], itemlist[index])
    
    outhandle.write(member_str+'\n');
    outhandle.close()

def genDao(itemdict, itemlist, typelist, tablename, daoname, prikey):
    outhandle= open(daoname+".py", "a+")
    #outhandle.write("\nclass %s:\n" % (tablename+"Dao"))
    #db get
    get_str = addtab(1) + "def get_%s(self, %s):" % (tablename, prikey)
    itemlen = len(itemlist)
    tab = 2
    get_str += addtab(tab)+ ("sql = \"Select * from account where %s = \'%s\'\" %% (%s)" % (prikey, formatFromType(itemdict[prikey]), prikey))

    get_str += addtab(tab)+"try:"+addtab(tab+1)+"self.__cursor.execute(sql)"+addtab(tab+1)+"results = self.__cursor.fetchall()"+addtab(tab+1)
    get_str += addtab(tab+1)+"if len(results) <= 0:"
    get_str += addtab(tab+2) + "return DB_GET_FAIL, None"
    get_str += addtab(tab+1)+"row = results[0]"
    for index in xrange(itemlen):
        get_str += addtab(tab+1) + "%s = row[%d]" % (itemlist[index], index)
    get_str += addtab(tab+1) + "st_%s = %s(" % (tablename, tablename)
    for index in xrange(itemlen):
        if index == itemlen - 1:
            get_str += "%s)" % (itemlist[index])
        else:
            get_str += "%s, " % (itemlist[index])
    get_str += addtab(tab+1) + "return DB_OK, st_%s" % (tablename)
    get_str += addtab(tab) + "except Exception, e:" + addtab(tab+1) + "return DB_GET_FAIL, None"
    outhandle.write(get_str+'\n')

    #db add
    ops = {
            "Insert", "Update", "Delete"
            };
    for op in ops:
        mod_str = ""
        if op == "Insert":
            func = addtab(1) + "def add_%s(self, st_%s):" % (tablename, tablename)
            pre = ""
            mid = ""
            post = ""
            for index in xrange(itemlen):
                if index == itemlen - 1:
                    pre += itemlist[index] + ") Values ("
                    mid += "\'%s\')\" %% (" % (formatFromType(itemdict[itemlist[index]]))
                    post += "st_%s.%s)" % (tablename, itemlist[index]) 
                else:
                    pre += '%s, ' % (itemlist[index])
                    mid += "\'%s\', " % (formatFromType(itemdict[itemlist[index]]))
                    post += "st_%s.%s, " % (tablename, itemlist[index]) 
            sql = addtab(2)+"sql = \"Insert Into %s(" % (tablename) + pre + mid + post
            err_code = "DB_ADD_FAIL"

        elif op == "Update":
            func = addtab(1) + "def update_%s(self, st_%s):" % (tablename, tablename)
            pre = ""
            mid = "Where %s = \'%s\'\" %% (" % (prikey, formatFromType(itemdict[prikey]))
            post = ""
            for index in xrange(itemlen):
                if index == itemlen - 1:
                    pre += "%s = \'%s\' " % (itemlist[index], formatFromType(itemdict[itemlist[index]]))

                    post += "st_%s.%s, " % (tablename, itemlist[index]) 
                else:
                    pre += "%s = \'%s\', " % (itemlist[index], formatFromType(itemdict[itemlist[index]]))
                    post += "st_%s.%s, " % (tablename, itemlist[index]) 
            sql = addtab(2)+"sql = \"Update %s Set " % (tablename) + pre + mid + post + ("st_%s.%s)" % (tablename, prikey))
            err_code = "DB_UPDATE_FAIL"
        elif op == "Delete":
            func = addtab(1) + "def del_%s(self, st_%s):" % (tablename, tablename)
            sql = addtab(2)+"sql = \"Delete From %s where %s = \'%s\'\" %% (%s)" % (tablename, prikey, formatFromType(itemdict[prikey]), prikey)
            err_code = "DB_DEL_FAIL"

        mod_str = func + sql + addtab(2) + "try:" + addtab(3) + "self.__cursor.execute(sql)" + addtab(3) + "self.__db.commit()" + addtab(3) + "return DB_OK" + addtab(2) + "except Exception, e:" + addtab(3) + "self.__db.rollback()" + addtab(2) + "return %s" % (err_code)+'\n'
    
        outhandle.write(mod_str)

def genService(itemdict, itemlist, typelist, tablename, servicename, prikey):
    outhandle = open(servicename+".py", "a+")
    #update 
    update_str = addtab(1) + "def %s_update(self, request, headers):" % (tablename)
    update_str += addtab(2) + "query_dict = request.form"
    update_str += addtab(2) + "try:"

    update_str += addtab(3) + "if query_dict.get(\"%s\", None) is None:"  % (prikey.lower())
    update_str += addtab(4) + "ret_dict = {\"responseStr\":\"Update_failed\"}"
    update_str += addtab(4) + "json.dumps(ret_dict)" + addtab(4) + "return json_ret"

    update_str += addtab(3) + "ret, %s_info = self.__dao.get_%s(int(query_dict[\"%s\"]))" % (tablename, tablename, prikey.lower())
    update_str += addtab(3) + "if ret != 0:"
    update_str += addtab(4) + "ret_dict = {\"responseStr\":\"Update_failed\"}" + addtab(4) + "return json.dumps(ret_dict)"

    for index in xrange(len(itemlist)):
        update_str += addtab(3) + "if query_dict.get(\"%s\") != None:" % (itemlist[index].lower())
        update_str += addtab(4) + "%s_info.%s = %s(query_dict.get(\"%s\"))" % (tablename, itemlist[index], changeFromType(itemdict[itemlist[index]]), itemlist[index].lower())

    update_str += addtab(3) + "ret = self.__dao.update_%s(%s_info)" % (tablename, tablename)
    update_str += addtab(3) + "if ret == 0:"
    update_str += addtab(4) + "ret_dict = {\"responseStr\":\"Success\"}"
    update_str += addtab(3) + "else:"
    update_str += addtab(4) + "ret_dict = {\"responseStr\":\"Update_failed\"}"
    update_str += addtab(3) + "json.dumps(ret_dict)" + addtab(3) + "return json_ret"
    update_str += addtab(2) + "except Exception, e:" + addtab(3) + "print str(e)"
    update_str += addtab(3) + "ret_dict = {\"responseStr\":\"Update_failed\"}" + addtab(3) + "return json.dumps(ret_dict)"


    #get
    get_str = addtab(1) + "def %s_get(self, request, headers):" % (tablename)
    get_str += addtab(2) + "query_dict = request.query_dict"
    get_str += addtab(2) + "try:"

    get_str += addtab(3) + "if query_dict.get(\"%s\", None) is None:" % (prikey.lower())
    get_str += addtab(4) + "ret_dict = {\"responseStr\":\"Add_failed\"}"
    get_str += addtab(4) + "json.dumps(ret_dict)" + addtab(4) + "return json_ret"

    get_str += addtab(3) + "ret, %s_info = self.__dao.get_%s(int(query_dict[\"%s\"]))" % (tablename, tablename, prikey.lower())
    get_str += addtab(3) + "if ret != 0:"
    get_str += addtab(4) + "ret_dict = {\"responseStr\":\"Get_failed\"}" + addtab(4) + "return json.dumps(ret_dict)"

    get_str += addtab(3) + "ret_dict = {\"responseStr\":\"Success\"}"
    for index in xrange(len(itemlist)):
        get_str += addtab(3) + "ret_dict[\"%s\"] = %s_info.%s" % (itemlist[index].lower(), tablename, itemlist[index])

    get_str += addtab(3) + "json.dumps(ret_dict)" + addtab(3) + "return json_ret"
    get_str += addtab(2) + "except Exception, e:" + addtab(3) + "print str(e)"
    get_str += addtab(3) + "ret_dict = {\"responseStr\":\"Get_failed\"}" + addtab(3) + "return json.dumps(ret_dict)"



    #add
    add_str = addtab(1) + "def %s_add(self, request, headers):" % (tablename)
    add_str += addtab(2) + "query_dict = request.form"
    add_str += addtab(2) + "try:"

    add_str += addtab(3) + "%s_info = %s()" % (tablename, tablename)

    for index in xrange(len(itemlist)):
        add_str += addtab(3) + "if query_dict.get(\"%s\") != None:" % (itemlist[index].lower())
        add_str += addtab(4) + "%s_info.%s = %s(query_dict.get(\"%s\"))" % (tablename, itemlist[index], changeFromType(itemdict[itemlist[index]]), itemlist[index].lower())

    add_str += addtab(3) + "ret = self.__dao.add_%s(%s_info)" % (tablename, tablename)
    add_str += addtab(3) + "if ret == 0:"
    add_str += addtab(4) + "ret_dict = {\"%s\": %sinfo.%s,\n\"responseStr\":\"Success\"}" % (prikey.lower(), tablename, prikey)
    add_str += addtab(3) + "else:"
    add_str += addtab(4) + "ret_dict = {\"responseStr\":\"Add_failed\"}"
    add_str += addtab(3) + "json.dumps(ret_dict)" + addtab(3) + "return json_ret"
    add_str += addtab(2) + "except Exception, e:" + addtab(3) + "print str(e)"
    add_str += addtab(3) + "ret_dict = {\"responseStr\":\"Add_failed\"}"
    add_str += addtab(3) + "json.dumps(ret_dict)" + addtab(3) + "return json_ret"

    #delete
    del_str = addtab(1) + "def %s_del(self, request, headers):" % (tablename)
    del_str += addtab(2) + "query_dict = request.query_dict"
    del_str += addtab(2) + "try:"

    del_str += addtab(3) + "if query_dict.get(\"%s\", None) is None:" % (prikey.lower())
    del_str += addtab(4) + "ret_dict = {\"responseStr\":\"Del_failed\"}"
    del_str += addtab(4) + "json.dumps(ret_dict)" + addtab(4) + "return json_ret"

    del_str += addtab(3) + "ret = self.__dao.del_%s(int(query_dict[\"%s\"]))" % (tablename, prikey.lower())
    del_str += addtab(3) + "if ret != 0:"
    del_str += addtab(4) + "ret_dict = {\"responseStr\":\"Del_failed\"}" + addtab(4) + "return json.dumps(ret_dict)"

    del_str += addtab(3) + "ret_dict = {\"responseStr\":\"Success\"}"

    del_str += addtab(3) + "json.dumps(ret_dict)" + addtab(3) + "return json_ret"
    del_str += addtab(2) + "except Exception, e:" + addtab(3) + "print str(e)"
    del_str += addtab(3) + "ret_dict = {\"responseStr\":\"Del_failed\"}"
    del_str += addtab(3) + "json.dumps(ret_dict)" + addtab(3) + "return json_ret"

    outhandle.write(update_str+'\n')
    outhandle.write(get_str+'\n')
    outhandle.write(add_str+'\n')
    outhandle.write(del_str+'\n')
    outhandle.close()


def main():
    command = sys.argv[1]
    tablename = sys.argv[2]
    itemdict, itemlist, typelist, prikey = getDict(tablename)
    #gen db struct
    if (command == "comm"):
        commname = sys.argv[3]
        genClass(itemdict, itemlist, tablename, commname)
    #gen db operator
    elif (command == "dao"):
        daoname = sys.argv[3]
        genDao(itemdict, itemlist, typelist, tablename, daoname, prikey)
    #gen service operator
    elif (command == "service"): 
        servicename = sys.argv[3]
        genService(itemdict, itemlist, typelist, tablename, servicename, prikey)

if __name__ == '__main__':
    main()
