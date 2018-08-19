#encoding: utf-8

import time
from datetime import datetime

#-------------------------------时间戳转换为指定格式日期---------------------------

#获得当前时间时间戳
def get_stamp():
    return int(time.time())

#转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
def stamp_to_strftime(timeStamp):
    timeStruct = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)


#---------------------------获取当前时间并转换为指定日期格式--------------------------
#time格式化成指定格式
def strftime(format,in_time):
    return time.strftime(format, in_time)

#time格式化为默认格式"%Y-%m-%d %H:%M:%S"
def format_time(in_time):
    return time.strftime("%Y-%m-%d %H:%M:%S", in_time)

#time格式化为默认格式"%Y-%m-%d %H:%M:%S"
def format_date(obj):
    return obj.strftime("%Y-%m-%d %H:%M:%S")
    # return time.strftime("%Y-%m-%d %H:%M:%S", in_time)

def get_localtime():
    return format_time(time.localtime())


#-----------------------------------格式切换------------------------------------------
def format_to(t,format1,format2):
    #t = "2017-11-24 17:30:00"
    # 先转换为时间数组,然后转换为其他格式
    #timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    timeStruct = time.strptime(t, format1)
    #strTime = time.strftime("%Y/%m/%d %H:%M:%S", timeStruct)
    return time.strftime(format2, timeStruct)



#--------------------------将字符串的时间转换为时间戳--------------------------------

def strftime_to_stamp(t):
    #t = "2017-11-24 17:30:00"
    # 将其转换为时间数组
    timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳:
    return int(time.mktime(timeStruct))




# print('stamp:',get_stamp())
#
# print(time.time())
# print(get_localtime())
