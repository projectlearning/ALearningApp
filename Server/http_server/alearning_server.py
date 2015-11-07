import socket
import select
import os, sys, re
import Queue
import thread, threading
import traceback
from multiprocessing import cpu_count
import time
import errno
import cgi
from StringIO import StringIO
import logging
import getopt
import json

import accountservice

sys.path.append("../util")
from util import *

#import account_pb2

#thread_num = 2 * cpu_count()
ERR_HTTP_READ = -10001
ERR_HTTP_DATANEED = -10002
ERR_HTTP_OK = 0

logger = logging.getLogger("http-server")
thread_num = 1
MaxReadSize = 1024 * 1024 * 1024
static_file_dir = "static"

static_dir = "/%s/" % static_file_dir
read_cache_dir = "read_cache"
cache_static_dir = "cache_%s" % static_file_dir
if not os.path.exists(cache_static_dir):
    os.makedirs(cache_static_dir)
if not os.path.exists(read_cache_dir):
    os.makedirs(read_cache_dir)

action_time = {}
filelist = os.listdir("./")
for filename in filelist:
    if filename == str(__file__): #self file
        continue
    prefix, ext = os.path.splitext(filename)
    if ext == ".py":
        try:
            __import__(prefix)
            mtime = os.path.getmtime(filename)
            action_time[prefix] = mtime
        except Exception, e:
            print str(e) + getTraceStackMsg()
            continue

def loginit():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - [%(process)d-%(thread)d] - [%(funcName)s - %(lineno)d] - %(levelname)s - %(message)s")

    fh = logging.FileHandler("http-server.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def printdict(dic):
    for key, value in dic.items():
        print "(%s, %s)" % (key, value)

class Item(object):
    def __init__(self, param, epoll_fd, fd):
        self.param = param
        self.epoll_fd = epoll_fd
        self.fd = fd
    def get(self):
        return self.param, self.epoll_fd, self.fd

def http_parse(param, datas, read_len):
    len_s = -1
    len_e = -1 
    contentlen = param.get("contentlen", -1)
    headlen = param.get("headlen", -1)

    if contentlen == -1:
        len_s = datas.find("Content-Length:")
        if len_s < 0:
            len_s = datas.lower().find("content-length:")
        if len_s > 0:
            len_e = datas.find("\r\n", len_s)
        if len_s > 0 and len_e > 0 and len_e > len_s + 15: # 15? 14?
            len_str = datas[len_s+15:len_e].strip()
            if len_str.isdigit():
                contentlen = int(datas[len_s+15:len_e].strip())
                param["contentlen"] = contentlen

    if contentlen > MaxReadSize:
        return ERR_HTTP_READ 

    if headlen == -1:
        headend = datas.find("\r\n\r\n")
        if headend > 0:
            headlen = headend + 4
            param["headlen"] = headlen

    if contentlen + headlen > read_len:
        return ERR_HTTP_DATANEED

    if ": multipart/form-data; boundary" in datas and len(datas) > 1024 * 1024 * 3 and "rc" not in param:
        #if ": multipart/form-data; boundary" in datas and "rc" not in param:
        #print "hahah"
        if headlen > 0 and contentlen > 0:
            param["rc"] = open("%s/%s_%s.tmp" % (read_cache_dir, pid, fd), "w")
        else:
            return ERR_HTTP_READ

    if "rc" in param:
        param["rc"].write(datas)
        param["readdata"] = ""
    else:
        param["readdata"] = datas

    #param["readdata"] = datas
    toprocess = param.get("toprocess", "")
    #print contentlen, headlen, read_len
    if "" == toprocess and ((contentlen >= 0 and headlen > 0 and (contentlen + headlen) <= read_len) or (contentlen == -1 and headlen > 0 and headlen <= read_len)):

        if "rc" in param:
            param["rc"].close()
            param["read_cache_name"] = "%s/%s_%s.tmp" % (read_cache_dir, pid, fd)
            param["rc"] = open(param["read_cache_name"], "r")
            read_len = 0
        else:
            one_http_len = headlen
            if contentlen > 0:
                one_http_len += contentlen
            #print one_http_len, len(param["readdata"])
            param["toprocess"] = param["readdata"][0:one_http_len]
            param["readdata"] = param["readdata"][one_http_len:]
            read_len = read_len - one_http_len

    param["contentlen"] = -1
    param["headlen"] = -1
    param["read_len"] = read_len
    #print param["toprocess"]
    return ERR_HTTP_OK

class QuickHttpRequest(object):
    def __init__(self, res_headers, data, epoll_fd, fd):
        self.res_headers = res_headers
        self.data = data
        self.epoll_fd = epoll_fd
        self.fd = fd
        self.keepalive = False

    def parse(self, param):
        print "parse: \n", printdict(param)
        self.client_ip = param["addr"][0]
        self.client_port = param["addr"][1]
        
        headend = -1
        if "rc" in param:
            fp = param["rc"]
            data = ""
            while True:
                subdata = fp.read(1024)
                if subdata == "":
                    break
                data += subdata
                headend = data.find("\r\n\r\n")
                if headend > 0:
                    break
            fp.seek(0)
        else:
            data = param["toprocess"] 
            headend = data.find("\r\n\r\n")
            fp = StringIO(data)
        
        headlist = []
        if headend > 0: #have header
            headlist = data[0:headend].split("\r\n")
        else:
            headlist = data.split("\r\n")

        first_line = headlist.pop(0)
        self.command, self.path, self.http_version, = re.split('\s+', first_line)

        self.baseuri = self.path.split('?')[0]
        indexlist = self.baseuri.split('/')

        #print str(indexlist)

        while len(indexlist) != 0:
            self.index = indexlist.pop()
            if self.index == "":
                continue
            else:
                self.action, self.method = os.path.splitext(self.index)
                self.method = self.method.replace('.', '')
                break

        self.headers = {}
        
        for item in headlist:
            if item.strip() == "":
                continue
            segindex = item.find(":")
            if segindex < 0:
                continue
            key = item[0:segindex].strip()
            value = item[segindex+1:].strip()
            self.headers[key.lower()] = value

        #logger.debug(str(self.headers))
        #if self.headers.get("connection", "") == "keep-alive":
        #    self.keepalive = True
   
        self.command = self.command.lower()

        logger.debug("self.command: %s, self.path: %s, self.http_version: %s, self.action: %s, self.method: %s, self.headers: %s" % (self.command,  self.path, self.http_version, self.action, self.method, self.headers))

        self.query_dict = dict()
        self.form = dict()
        self.filedic = dict()
        self.query_dict.clear()
        self.form.clear()
        self.filedic.clear()
        self.body = ""

        #print "ison: post: %s, method: %s" % (self.command, self.method)
        
        if self.command == "get" and "?" in self.path:
            parse_query(self.path.split("?").pop(), self.query_dict)
            #print str(self.query_dict)
        elif self.command == "post" and self.headers.get('content-type',"").find("boundary") > 0:
            cgiform = cgi.FieldStorage(fp=fp, headers=None, environ={'REQUEST_METHOD': self.command, 'CONTENT_TYPE': self.headers['content-type'], })
            for key in cgiform:
                fileitem = cgiform[key]
                if fileitem.filename == None:
                    self.form[key] = fileitem.file.read()
                    #print self.form[key]
                else:
                    self.filedic[key] = fileitem
                    #print fileitem
                    #print fileitem.file
                    #print fileitem.name, fileitem.filename
        elif self.command == "post":
            self.body = data[headend+4:]
            logger.debug("self.body: %s" % (self.body))
            #parse_query(self.body, self.form)
            self.form = json.loads(self.body)
            print self.body, self.form

class Worker(object):
    def __init__(self):
        self._obj_dict = {}
        self._mtime_dict = {}

        for filename in filelist:
            if filename == str(__file__): #self file
                continue
            prefix, ext = os.path.splitext(filename)
            #print prefix, ext
            if ext == ".py" and prefix in sys.modules:
                try:
                    action = sys.modules[prefix]
                    self._obj_dict[prefix] = eval("action.%s()" % prefix)
                    self._mtime_dict[prefix] = action_time[prefix]
                except Exception, e:
                    print str(e) + getTraceStackMsg()
                    continue


    def getGloabalAction(self, action_key):
        action = sys.modules.get(action_key, None)
        #if action == None:
        #    print 1
        #else:
        #    print str(action)
        auto_update = False
        if action == None:
            auto_update = True
        else:
            try: 
                auto_update = action.FastpyAutoUpdate
            except Exception, e:
                pass

        if not auto_update:
            return auto_update, None, None
        if action == None:
            #print "test1: ", action, action_key
            action = __import__(action_key)
            #print "test2: ", action
            mtime = os.path.getmtime("./%s.py" % action_key)
            action_time[action_key] = mtime
        else:
            load_time = action_time[action_key]
            mtime = os.path.getmtime("./%s.py" % action_key)
            if mtime > load_time:
                try:
                    del sys.modules[action_key]
                    del action
                except Exception, e:
                    pass
                action = __import__(action_key)
                action_time[action_key] = mtime
        return auto_update, action, mtime

    def process(self, data, epoll_fd, fd):
        #return
        res = ""
        add_head = ""
        headers = {}
        try:
            request = QuickHttpRequest(headers, data, epoll_fd, fd)
            request.parse(data)
        except Exception, e:
            print str(e) + getTraceStackMsg()
            res = "http format error"

        try:
            #logger.debug("headers: %s, request.res_headers: %s" % (headers, request.res_headers))
            #headers["Content-Type"] = "text/html;charset=utf-8"
            headers["Content-Type"] = "application/json"
            headers["Access-Control-Allow-Origin"] = "*"
            if request.keepalive == True:
                headers["Connection"] = "keep-alive"

            action_key = request.action
            #obj = self._obj_dict.get(action_key, None)
            #print data
            #print action_key
            obj = data.get(action_key, None)
            
            #print obj
            #print dir(obj)
            load_time = self._mtime_dict.get(action_key, None)

            auto_update, action, mtime = self.getGloabalAction(action_key)

            if auto_update and (obj == None or load_time == None or mtime > load_time):
                self._mtime_dict[action_key] = mtime
                obj = eval("action.%s()" % action_key)
                self._obj_dict[action_key] = obj

            print action_key, str(obj)
            method = getattr(obj, request.method)
            res = method(request, headers)

            if res == None:
                return None

        except Exception, e:
            logger.error(str(e) + getTraceStackMsg())
            res = "404 Not Found"

        try:
            if headers.get("Connection", "") == "keep-alive":
                data["keepalive"] = True
            else:
                data["keepalive"] = False
            print res
            res_len = len(res)
            headers["Content-Length"] = res_len
            for key in headers:
                add_head += "%s: %s\r\n" % (key, headers[key])
            if res == "404 Not Found":
                data["writedata"] = "HTTP/1.1 404 Not Found\r\n%s\r\n%s" % (add_head, res)
            else:
                data["writedata"] = "HTTP/1.1 200 OK\r\n%s\r\n%s" % (add_head, res)
            print "response data: %s" % data["writedata"]
        
            epoll_fd.modify(fd, select.EPOLLOUT | select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
        except Exception, e:
            print str(e) + getTraceStackMsg()

class MyThread(threading.Thread):
    def __init__(self, threadCondition, shareObject, **kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        self.shareObject = shareObject
        self.setDaemon(True)
        self.worker = Worker()

    def processer(self, param, epoll_fd, fd):
        #print "processer"
        try:
            #print "MyThread.process" 
            self.worker.process(param, epoll_fd, fd)
        except:
            print "job error:" + getTraceStackMsg()
    
    def run(self):
        while True:
            try:
                #print "1MyThread.run" 
                item = self.shareObject.get()
                param, epoll_fd, fd = item.get()
                #print "MyThread.run" 
                self.processer(param, epoll_fd, fd)
            except Queue.Empty:
                print "Queue.Empty"
                continue
            except Exception, e:
                pass
                print str(e)
                print "thread error"
                #print "thread error:" + getTraceStackMsg()

class ThreadPool:
    def __init__(self, num_of_threads=2):
        self.threadCondition = threading.Condition()
        self.shareObject = Queue.Queue()
        self.threads = []
        self.__createThreadPool(num_of_threads)

    def __createThreadPool(self, num_of_threads):
        for i in xrange(num_of_threads):
            thread = MyThread(self.threadCondition, self.shareObject)
            self.threads.append(thread) 
    
    def start(self):
        for thread in self.threads:
            thread.start()
    
    def add_job(self, param, epoll_fd, fd):
        #print "ThreadPool.add_job"
        self.shareObject.put(Item(param, epoll_fd, fd))

def check_next_http(param, tp, epoll_fd, fd, work):
    print "check next"
    datas = param.get("readdata", "")
    if "" == datas:
        param["toprocess"] = ""
        return 0
    read_len = len(datas)
    contentlen = param.get("contentlen", -1)
    headlen = param.get("headlen", -1)
    if contentlen == -1:
        len_s = datas.find("Content-Length:")
        if len_s < 0:
            len_s = datas.lower().find("content-length:")
        if len_s > 0:
            len_e = datas.find("\r\n", len_s)
        if len_s > 0 and len_e > 0 and len_e > len_s+15:
            len_str = datas[len_s+15:len_e].strip()
            if len_str.isdigit():
                contentlen = int(datas[len_s+15:len_e].strip())
                param["contentlen"] = contentlen
    if headlen == -1:
        headend = datas.find("\r\n\r\n")
        if headend > 0:
            headlen = headend + 4
            param["headlen"] = headlen
    if (contentlen >= 0 and headlen > 0 and (contentlen + headlen) <= read_len) or \
           (contentlen == -1 and headlen > 0 and headlen <= read_len):
        one_http_len = headlen
        if contentlen > 0:
            one_http_len += contentlen
        param["toprocess"] = param["readdata"][0:one_http_len]
        param["readdata"] = param["readdata"][one_http_len:read_len]
        read_len = read_len - one_http_len
        param["contentlen"] = -1
        param["headlen"] = -1
        param["read_len"] = read_len
        tp.add_job(param,epoll_fd,fd)
        #work.process(param,epoll_fd,fd)
        return one_http_len
    else:
        param["toprocess"] = ""
        return 0


def clearfd(epoll_fd, params, fd):
    try:
        epoll_fd.unregister(fd)
    except Exception, e:
        print str(e)
        pass

    try:
        param = params[fd]
        #print "clearfd: %d, param: %s\n\n" % (fd, str(param))
        #printdict(param)
        logger.debug("%d connection close\n" % param["connections"].fileno())
        param["connections"].close()
    except Exception, e:
        print str(e)
        pass

    try: 
        del params[fd]
    except Exception, e:
        pass

def run_main(listen_fd, service):
    try:
        epoll_fd = select.epoll()
        epoll_fd.register(listen_fd.fileno(), select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
    except select.error, msg:
        print "select.error" + getTraceStackMsg()

    tp = ThreadPool(thread_num)
    tp.start()
    work = Worker()
    pid = os.getpid()

    params = {}
    last_min_time = -1

    while True:
        epoll_list = epoll_fd.poll()

        cur_time = time.time()
        for fd, events in epoll_list:
            if fd == listen_fd.fileno():
                while True:
                    try:
                        conn, addr = listen_fd.accept()
                        conn.setblocking(0)
                        epoll_fd.register(conn.fileno(), select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
                        conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        params[conn.fileno()] = {"addr":addr, "writelen":0, "connections":conn, "time":cur_time, "accountservice":service}
                    except socket.error, msg:
                        break
            elif select.EPOLLIN & events:
                print "epollin"
                param = params.get(fd, None)
                #print "epollin: %d, params: %s\n\n" % (fd, str(param))               
                #printdict(param)
                if param == None:
                    continue
                param["time"] = cur_time
                datas = param.get("readdata", "")
                #datas = ""
                #param["readdata"] = ""

                logger.debug("epollin datas: %s" % datas)
                #####
                cur_sock = param.get("connections", None)
                read_len = param.get("read_len", 0)
                while True:
                    try:
                        data = cur_sock.recv(102400)
                        if not data and not datas:
                            logger.debug("--------------------test1---------------------")
                            clearfd(epoll_fd, params, fd)
                            break
                        else:
                            logger.debug("fd: %d, read---------------%s" % (fd, data))
                            datas += data
                            read_len += len(data)
                    except socket.error, msg:
                        if msg.errno == errno.EAGAIN:
                            #print datas
                            #print datas
                            success_parse = http_parse(param, datas, read_len)
                            if success_parse == ERR_HTTP_OK:
                                tp.add_job(param, epoll_fd, fd) 
                                #datas = ""
                            elif success_parse == ERR_HTTP_DATANEED:
                                continue
                            else:
                                logger.error("--------------------test2---------------------")
                                clearfd(epoll_fd, params, fd)
                        else:
                            logger.error("--------------------test3---------------------")
                            clearfd(epoll_fd, params, fd)
                        break
            elif select.EPOLLHUP & events or select.EPOLLERR & events:
                logger.error("hup or err")
                clearfd(epoll_fd, param, fd)
            elif select.EPOLLOUT & events:
                param = params.get(fd, None)
                if param == None:
                    continue
                param["time"] = cur_time
                sendLen = param.get("writelen", 0)
                writedata = param.get("writedata", "")
                #print sendLen, writedata
                total_write_len = len(writedata)
                cur_sock = param["connections"]
                totalsenlen = param.get("totalsenlen", None)

                if writedata == "":
                    logger.error("--------------------test4---------------------")
                    clearfd(epoll_fd, params, fd)
                    continue
                while True:
                    try: 
                        sendLen += cur_sock.send(writedata[sendLen:])
                        if sendLen == total_write_len:
                            print "sendlen: %s" % sendLen
                            if param.get("keepalive", True): #default: keep alive
                                logger.debug("keepalive")
                                param["writedata"] = ""
                                param["writelen"] = 0
                                epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
                                #check_next_http(param, tp, epoll_fd, fd, work)
                                ######
                            else:
                                logger.error("--------------------test5---------------------")
                                clearfd(epoll_fd, params, fd)
                            break

                    except socket.error, msg:
                        if msg.errno == errno.EAGAIN:
                            param["writelen"] = sendLen
                        else:
                            logger.error("--------------------test6---------------------")
                            clearfd(epoll_fd, params, fd)
                        break
            else:
                continue

        if cur_time - last_min_time > 600:
            last_min_time = cur_time
            objs = params.items()
            for (key_fd, value) in objs:
                fd_time = value.get("time", 0)
                del_time = cur_time - fd_time
                if del_time > 600:
                    logger.error("--------------------test6---------------------")
                    clearfd(epoll_fd, params, key_fd)
                elif fd_time < last_min_time:
                    last_min_time = fd_time


def usage():
    pass

def init_as_daemon():
    pid = os.fork()
    if pid > 0:
        sys.exit(pid)

    #os.chdir("/")
    os.setsid()
    os.umask(0)

    pid = os.fork()
    if pid > 0:
        sys.exit(pid)

    sys.stdout.flush()
    sys.stderr.flush()
    si = file("/dev/null", 'r')
    so = file("/dev/null", 'a+')
    se = file("/dev/null", 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    loginit()
   
    opts, args = getopt.getopt(sys.argv[1:], "hdi:p:", ["help"])
    configname = ""
    port = 8989

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print usage() 
        elif opt == '-i':
            configname = arg
            print configname
        elif opt == '-p':
            port = int(arg)
        elif opt == '-d':
            init_as_daemon()
    
    try:
        listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error, msg:
        logger.error("create socket failed")
    try:
        listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error, msg:
        logger.error("setsocketopt SO_REUSEADDR failed")
        
    try:
        listen_fd.bind(('', port))
    except socket.error, msg:
        logger.error("bind failed") 
    try:
        listen_fd.listen(10240)
        listen_fd.setblocking(0)
    except socket.error, msg:
        logger.error(msg) 

    

    #child_num = cpu_count()
    #c = 0
    #while c < child_num:
    #    c = c + 1
    #    newpid = os.fork()
    #    if newpid == 0:
    #        run_main(listen_fd)

    service = accountservice.accountservice(configname)
    run_main(listen_fd, service)
                            
