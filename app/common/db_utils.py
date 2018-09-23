#from fly_bbs.extensions import mongo
#from bson.objectid import ObjectId
from app.common.utils import JSONEncoder
from flask import request
from datetime import datetime
from app.common.json_utils import list_to_json

class Page:
    def __init__(self, pn, size, sort_by=None, filter1=None, result=None, has_more=False, total_page=0, total=0):
        self.page = pn
        self.size = size
        self.sort_by = sort_by
        self.result = result
        self.filter1 = filter1
        self.has_more = has_more
        self.total_page = total_page
        self.total=total

    def __repr__(self):
        return JSONEncoder().encode(o = self.__dict__)


def pages(obj,req,sort_by=('created_time','desc'), filter1=None):
   # _process_filter(filter1)
    page_size = req.args.get('limit', 10, type=int)
    page = req.args.get('page', 1, type=int)

    if not (hasattr(obj,sort_by[0]) and sort_by[1].lower() in ['desc','asc']):
        return

    pagination = obj.query.order_by(getattr(getattr(obj,sort_by[0]),sort_by[1])()).paginate(
        page, per_page=page_size, error_out=False)

    # pagination = res.paginate(
    #     page, per_page=page_size, error_out=False)

    #comments = pagination.items

    #result1 = [item.to_json() for item in pagination.items]
    result = list_to_json(pagination.items)
    total = pagination.total
    total_page = int(total /page_size)
    if total % page_size > 0:
        total_page = total_page + 1
    page = Page(page, page_size, sort_by=sort_by, filter1={}, result=list(result),total_page=total_page,total=total)
    return page


# def _process_filter(filter1):
#     if filter1 is None:
#         return
#     _id = filter1.get('_id')
#     if _id and not isinstance(_id, ObjectId):
#         filter1['_id'] = ObjectId(_id)


# def get_option(name, default=None):
#     return mongo.db.options.find_one({'code': name}) or default


# def get_page(collection_name, pn=1, size=10, sort_by=None, filter1=None):
#     _process_filter(filter1)
#     if size <= 0:
#         size = 15
#     total = mongo.db[collection_name].count(filter1)
#     # print(total)
#     skip_num = (pn - 1) * size
#     result = []
#     has_more = total > pn * size
#     if total - skip_num > 0:
#         result = mongo.db[collection_name].find(filter1, limit=size)
#         if sort_by:
#             result = result.sort(sort_by[0], sort_by[1])
#
#         if skip_num >= 0:
#             result.skip(skip_num)
#
#     total_page = int(total / size)
#     if total % size > 0:
#         total_page = total_page + 1
#     page = Page(pn, size, sort_by, filter1, list(result), has_more, total_page, total)
#     return page


# def get_list(collection_name, sort_by=None, filter1=None, size=None):
#     _process_filter(filter1)
#     result = mongo.db[collection_name].find(filter1)
#     if sort_by:
#         result = result.sort(sort_by[0], sort_by[1])
#     if size:
#         result = result.limit(size)
#     result = list(result)
#     return result
#
#
# def find_one(collection_name, filter1=None):
#     _process_filter(filter1)
#     return mongo.db[collection_name].find_one(filter1)