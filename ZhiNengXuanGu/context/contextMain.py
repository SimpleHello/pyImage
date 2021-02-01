# coding=UTF-8

import logging

from context import contextSpider

logging.basicConfig()


def startIndex():
    var_list = ContextJson.readId()
    for ids in var_list:
        x = ids.get("id")
        contextSpider.demoSimple()
        contextSpider.getAiIndex('%d' % x)


def startIndex2():
    contextSpider.getAiIndex('64589')


def initDemo():
    contextSpider.demoSimple()


if __name__ == '__main__':
    initDemo()
