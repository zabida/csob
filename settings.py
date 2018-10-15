# coding:utf-8

# 该文件用于存放系统相关的配置信息

MQTTSERVICE_HOST = "192.2.4.194"
MQTTSERVICE_PORT = 9999

DATA_HOST = "192.168.127.100"
DATA_PORT = 5050

_user = "80004817847300"
_pwd = "J0443120026"
# apscheduler时间参数配置
hour = "*"
minute = "*/10"  # 表示每隔2分钟执行一次该定时任务框架


# Expression	Field	Description
# *	        any	Fire on every value
# */a	        any	Fire every a values, starting from the minimum
# a-b	        any	Fire on any value within the a-b range (a must be smaller than b)
# a-b/c	    any	Fire every c values within the a-b range
# xth y	    day	Fire on the x -th occurrence of weekday y within the month
# last x	    day	Fire on the last occurrence of weekday x within the month
# last	    day	Fire on the last day within the month
# x,y,z	    any	Fire on any matching expression; can combine any number of any of the above expressions

