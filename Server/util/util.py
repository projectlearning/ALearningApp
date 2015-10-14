import sys
sys.path.append("../util")
from comm import *
import traceback


def getTraceStackMsg():
    tb = sys.exc_info()[2]
    msg = ''
    for i in traceback.format_tb(tb):
        msg += i
    return msg

def parse_query(query_str, query_dict):
    items = query_str.split("&")
    for item in items:
        if item == None or item == "" or "=" not in item:
            continue
        key_value = item.split("=")
        key = (key_value[0])
        #key = unquote(key_value[0])
        value = (key_value[1])
        #value = unquote(key_value[1])
        query_dict[str(key)] = str(value)

def struct2json(struct):
    json_ret = "{"
    for key in struct.__dict__:
        if key[0] != '_':
            json_ret += '"' + key + '" : ' + str(struct.__dict__[key])+','
    json_ret[len(json_ret)-1] = '}'
    return json_ret


