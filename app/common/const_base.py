#！/usr/bin/python
# -*- coding: utf-8 -*-

class _const(object):
    class ConstError(PermissionError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            raise self.ConstError("Can not change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError("const name %s is not all upper" % name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError("Can't unbind const(%s)" % name)
        raise NameError(name)

    def __getattr__(self, key):
        if key in self.__dict__.keys():
            return self.key
        else:
            return None

import sys
sys.modules[__name__] = _const()

