# _*_ coding:utf-8 _*_

import mysqlDb

str = "create table user003(id int,name VARCHAR(20))"
mysl = mysqlDb.Mysql()
mysl._exeCuteCommit(str)
