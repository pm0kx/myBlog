#encoding: utf-8

import os
import inspect
from functools import wraps
from flask import abort
from flask_login import current_user
from flask import render_template, request, jsonify

# from app.models import Action

#https://blog.csdn.net/hyman_c/article/details/54097878
#https://www.cnblogs.com/wuxie1989/p/6439618.html

def get_type(func):
    # action_type = os.getcwd().split("\\")[-1]
    return func.__module__.split(".")[-2]

def permission_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if not current_user.check(get_type(func),func.__name__):
            abort(403)
        return func(*args, **kwargs)
    return decorator


class Permission(object):

    def __init__(self,type=None, action=None):
        self.type = type
        self.action = action

    def check(self, type, func):
        if not current_user:
            return False
        return current_user.check(type,func)

    def deny(self):
        #return render_template('403.html'), 403
        return '403'

    def __call__(self, func):
        #action_type = get_type(func)
        @wraps(func)
        def decorator(*args, **kwargs):
            if not self.check(get_type(func), func.__name__):
                return self.deny()
            return func(*args, **kwargs)
        return decorator

    def __enter__(self):
        if not self.check(self.type, self.action):
            try:
                self.deny()
            except Exception as e:
                print(e)

    def __exit(self):
        pass

    # @property
    # def current_user(self):
    #     return g.user

permission = Permission()


# def admin_required(f):
#     return permission_required(Action.ADMIN)(f)


# @main.route('/forbid',methods=['GET','POST'])
# @login_required
# @permission_required(Permission.FORBID)
# def forbid():
#     return 'Hello World'
#
# @main.route('/forbid',methods=['GET','POST'])
# @login_required
# @permission_required(Permission.FORBID)
# def forbid():
#     return 'Hello World'