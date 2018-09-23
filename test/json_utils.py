# encoding: utf-8

from datetime import datetime

#参考：https://blog.csdn.net/chenyulancn/article/details/8203763


# def to_dict(obj):
#     return obj.__dict__

def attribute_to_json(obj):
    attributes = {}
    for attr in dir(obj):
        val = getattr(obj, attr)
        if not attr.startswith('__') \
                and not attr.startswith('_') \
                and not callable(val)\
                and attr not in ['metadata','query']:
            print(type(val))
            if isinstance(val,datetime):
                attributes[attr] = val.strftime("%Y-%m-%d %H:%M:%S")
            elif attr =='id':
                attributes[attr] = str(val)
            elif val =='':
                pass
            else:
                attributes[attr] = val
    print(attributes)
    return attributes


def to_dict(obj):
    if hasattr(obj,'to_json'):
        return obj.to_json()
    else:
        return attribute_to_json(obj)


def list_to_json(lst):
    if len(lst) >1:
        return [to_dict(item) for item in lst]
    else:
        return to_dict(lst[0])



