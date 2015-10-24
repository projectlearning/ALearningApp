import re, sys, os

class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self.segdict = dict()
        self.readfile()

    def readfile(self):
        fd = open(self.filename, "r")
        lines = fd.readlines()
        lastseg = None
        lastsegname = None
        for line in lines:
            line = line.lstrip()
            if len(line) <= 0:
                continue
            if line[0] == "#": #comment
                continue
            st = line.find('[')
            if st != -1:
                ed = line.find(']', st)
                lastsegname = line[st+1:ed] 
                self.segdict[lastsegname] = dict()

            else:
                if "=" not in line:
                    continue
                item = line.split("=")
                self.segdict[lastsegname][item[0].strip()] = item[1].strip()

    def getItem(self, segname, itemname):
        return self.segdict[segname][itemname]
        
    def printseg(self):
        print str(self.segdict)
        for key, value in self.segdict.items():
            for k, v in value.items():
                print k, v


            


