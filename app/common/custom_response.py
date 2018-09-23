#encoding: utf-8

from flask import  Response
from datetime import datetime
from flask_restful import abort
from app.common.json_utils import to_dict


class R(dict):

    @staticmethod
    def ok(data=None,msg=''):
        r = R()
        r.put('code', 0)
        r.put('msg', msg)
        r.put('data', data)
        return r

    @staticmethod
    def fail(code=404, msg=None):
        r = R()
        r.put('code', code)
        r.put('msg', msg)
        return r

    def put(self, k, v):
        self.__setitem__(k, v)
        return self

    def get_code(self):
        return self.get('code')

    def get_msg(self):
        return self.get('msg')


class BaseResult(R):
    def __init__(self, code=0, msg='', data=None):
        self.put('code', code)
        self.put('msg', msg)
        self.put('data', data)


# class ResponseCode:
#     SUCCESS = 0
#     ERROR =1
#     WRONG_PARAM = 400
#
#
# class ResponseMsg:
#     SUCCESS = 'ok!'
#     ERROR = 'param error'


# def to_json(obj):
#     if hasattr(obj,'to_json'):
#         return obj.to_json()
#     else:
#         return obj.__dict__
#
# def json_arr(lst,obj):
#     pass
#     if len(lst) >1:
#         return [to_json(item) for item in lst]
#     else:
#         return to_json(lst[0])

#
# def generate_response(obj=None,data=None, message=ResponseMsg.SUCCESS, code=ResponseCode.SUCCESS,count=1):
#     return {
#         'msg': message,
#         'code':code,
#         'count':count,
#         'data': json_arr(data,obj),
#         'time': datetime.now()
#     }


# def my_abort(http_status_code, *args, **kwargs):
#     if http_status_code == 400:
#         # 重定义400返回参数
#         abort(400, **generate_response(data=[kwargs.get('message')], message='参数错误！', code=http_status_code))
#
#     abort(http_status_code)







#参考https://blog.miguelgrinberg.com/post/customizing-the-flask-response-class

# class MyResponse(Response):
#     Access-Control-Allow-Origin = '*'
#     Access-Control-Allow-Methods = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
#     default_mimetype = 'application/json'
    # def __init__(self, response=None, **kwargs):
    #     kwargs['headers'] = ''
    #     headers = kwargs.get('headers')
    #     # 跨域控制
    #     origin = ('Access-Control-Allow-Origin', '*')
    #     methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
    #     if headers:
    #         headers.add(*origin)
    #         headers.add(*methods)
    #     else:
    #         headers = Headers([origin, methods])
    #     kwargs['headers'] = headers
    #     return super().__init__(response, **kwargs)