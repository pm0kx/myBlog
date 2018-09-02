#encoding: utf-8

# from flask import  Response
# from werkzeug.datastructures import Headers


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