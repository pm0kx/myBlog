#encoding: utf-8

from functools import wraps
from flask import abort
from flask_login import current_user
from app.models import Action

# def auth(method):
#     @wraps(method)
#     def wrapper(*args, **kwargs):
#         user_id = session.get('user_id')
#         if not user_id:
#             return abort(403)
#         return method(*args, **kwargs)
#     return wrapper


# def permission_required(permission):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not current_user.can(permission):
#                 abort(403)
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator


# def admin_required(f):
#     return permission_required(Action.ADMIN)(f)


permissions = list()

class Permission(object):

    def __init__(self, module=None, action=None):
        self.module = module
        self.action = action

    def check(self, module, func):
        if not self.current_user:
            return False
        return self.current_user.check('{module}.{action}'.format(
            module=module,
            action=func
        ))

    def deny(self):
        return fail(4003, '无权访问')

    def __call__(self, func):
        permissions.append({
            'action': '{}.{}'.format(func.__module__, func.__name__),
            'name': func.__doc__
        })
        @wraps(func)
        def decorator(*args, **kwargs):
            if not self.check(func.__module__, func.__name__):
                return self.deny()
            return func(*args, **kwargs)
        return decorator

    def __enter__(self):
        if not self.check(self.module, self.action):
            try:
                self.deny()
            except Exception as e:
                raise e
            else:
                raise PermissionDeniedException

    def __exit(self):
        pass

    @property
    def current_user(self):
        return g.user

permission = Permission()


# @app.router('/user/info')
# @permission
# def user_info():
#     """用户信息"""
#     return render_template('user/info.html')