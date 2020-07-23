# coding=UTF-8

import ContextIndex
import logging
import ContextJson

logging.basicConfig()



def startIndex():
    var_list = ContextJson.readId();
    for ids in var_list:
        x = ids.get("id")
        ContextIndex.getAiIndex('%d' % x)

def startIndex2():
    ContextIndex.getAiIndex('64589')


startIndex()
