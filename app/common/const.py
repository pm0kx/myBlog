#！/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path
import platform

from . import const_base as const


# 获取当前所处的文件夹的上一级绝对路径
const.ROOT_PATH=os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
const.ENABLED=1
const.DISENABLED=0
#根据操作系统分别处理
if platform.system()=='Windows':
    const._LOG_PATH = const.ROOT_PATH + '\logs\\'

elif platform.system() == 'Linux':
    const._LOG_PATH = os.path.join(const.ROOT_PATH ,'logs/')


LOG_PATH = const._LOG_PATH
ENABLED = const.ENABLED
DISENABLED = const.DISENABLED

#print(ROOT_PATH)
