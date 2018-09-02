#encoding: utf-8

from flask import render_template,request,current_app
from datetime import datetime
from flask import redirect,url_for,jsonify
from app.common import logger
from flask_login import login_url,current_user,login_required
from app.common.time_util import *
from sqlalchemy import func
from app.common.action_log import action_log

from . import admin
from app.models import User,Attachment,Catalog,Dictionary,ActionLog

logger = logger.Logger(logger="admin-common").getlog()

# @admin.route('/get_users',methods=['GET'])
# def users_page():
#     return render_template("admin/users.html")

@admin.route('/catalogs',methods=['GET'])
def catalog_list():
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)
    pagination = Catalog.query.order_by(Catalog.created_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    catalogs = pagination.items

    #prev = None
    #if pagination.has_prev:
    #    prev = url_for('admin.catalog_list', page=page - 1)
    #next = None
    #if pagination.has_next:
    #    next = url_for('admin.catalog_list', page=page + 1)
    return jsonify({
        'data': [catalog.to_json() for catalog in catalogs],
        'msg': '',
        'code': 0,
        'count': pagination.total,
        'time': get_localtime()
    })

@admin.route('/catalogs/<string:catalog_id>',methods=['GET'])
def get_catalog(catalog_id):
    catalog = Catalog.query.get_or_404(catalog_id)
    return jsonify(catalog.to_json())



@admin.route('/catalogs/<int:catalog_id>/dictionaries',methods=['GET'])
def get_dictionaries_by_catalog(catalog_id):
    dictionaries = Dictionary.query.filter(Dictionary.catalog_id == catalog_id)
    return jsonify({
        'data': [d.to_json() for d in dictionaries],
        'count': dictionaries.count(),
        'code':0,
        'msg':'',
        'time': get_localtime()
    })

@admin.route('/catalogs/',methods=['POST'])
def add_catalog():
    data = request.form.to_dict()
    name = data.get('name')
    catlog = Catalog.query.filter(Catalog.name == name).first()
    if catlog == None:
        cat = Catalog(name)
        cat.code = data.get('code')
        cat.is_show = data.get('is_show')
        cat.comments = data.get('comments')
        cat.created_time =datetime.now()
        db.session.add(cat)
        db.session.commit()
    else:
        return jsonify({
            'msg': 'catalog code exist !'
        })
    action_log(request, '添加字典目录')
    return jsonify({
        'msg': 'ok !'
    })

@admin.route('/catalogs/',methods=['PUT'])
def edit_catalog(catalog_id):
    data = request.form.to_dict()
    id = data.get('id')
    res = Catalog.query.filter(Catalog.id == id).first()
    is_update = False
    if not res == None:
        for attr, val in data.items():
            if hasattr(Catalog, attr):  # 检查实例是否有这个属性
                if not val == None:
                    setattr(Catalog, attr, val)  # same as: a.name =
                    is_update = True
        if is_update:
            res.modified_time = datetime.now()
            db.session.add(res)
            db.session.commit()
    else:
        return jsonify({
            'msg': 'res not exist !'
        })
    action_log(request, '修改菜单')
    return jsonify({
        'msg': 'ok !'
    })


@admin.route('/catalogs/<string:cat_id>',methods=['DELETE'])
def del_catalog(cat_id):
    res = Catalog.query.filter(Catalog.id == cat_id).first()
    if not res == None:
        # dicts=Dictionary.query.get(res.id)
        # res.dictionaries.remove(dicts)
        db.session.delete(res)
        db.session.commit()
    else:
        return 'error'
    return jsonify({
        'msg': 'ok !'
    })


#@admin.route('/dicts',methods=['GET'])
def get_dictionaries(name):
    dictionaries = Dictionary.query.join(Catalog).filter(Catalog.name == name)
    return jsonify({
        'data': [dictionary.to_json() for dictionary in dictionaries],
        'msg': '',
        'code': 0,
        'count': dictionaries.count(),
        'time': get_localtime()
    })

@admin.route('/catalogs/dictionary',methods=['POST'])
def add_dictionary():
    data = request.form.to_dict()
    code = data.get('code')
    dicts = Dictionary.query.filter(Dictionary.code == code).first()
    if dicts == None:
        d = Dictionary(data.get('name'))
        d.code = data.get('code')
        d.order = data.get('oder')
        d.catalog_id =data.get('catalog_id')
        d.created_time = datetime.now()
        db.session.add(d)
        db.session.commit()
    else:
        return jsonify({
            'msg': 'dictionary code exist !'
        })
    action_log(request, '添加字典')
    return jsonify({
        'msg': 'ok !'
    })

@admin.route('/catalogs/dictionary',methods=['PUT'])
def edit_dictionary(id):
    data = request.form.to_dict()
    id = data.get('id')
    res = Dictionary.query.filter(Dictionary.id == id).first()
    is_update = False
    if not res == None:
        for attr, val in data.items():
            if hasattr(Dictionary, attr):  # 检查实例是否有这个属性
                if not val == None:
                    setattr(Dictionary, attr, val)  # same as: a.name =
                    is_update = True
        if is_update:
            res.modified_time = datetime.now()
            db.session.add(res)
            db.session.commit()
    else:
        return jsonify({
            'msg': 'dict not exist !'
        })
    action_log(request, '修改字典')
    return jsonify({
        'msg': 'ok !'
    })

@admin.route('/catalogs/dictionary<string:id>',methods=['DELETE'])
def del_dictionary(id):
    res = Dictionary.query.filter(Dictionary.id == id).first()
    if not res == None:
        db.session.delete(res)
        db.session.commit()
    else:
        return 'error'
    return jsonify({
        'msg': 'ok !'
    })


@admin.route('/logs',methods=['GET'])
def actionlog_list():
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)
    pagination = ActionLog.query.order_by(ActionLog.action_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    logs = pagination.items

 
    return jsonify({
        'data': [log.to_json() for log in logs],
        'msg': '',
        'code': 0,
        'count': pagination.total,
        'time': get_localtime()
    })



# @admin.route('/catalogs/bind-dict/',methods=['POST'])
# def bind_dictionary_to_catalog():
#     data = request.form.to_dict()
#     type = data.get('type')
#     cat_id = data.get('catalog_id')
#     cat = Catalog.query.filter(Catalog.id == cat_id).first()
#     dict_id_list = data.get('dict_id')
#
#     if type == 'bind' and cat:
#         if isinstance(list, dict_id_list):
#             dicts = Dictionary.query.filter(Dictionary.id.in_(dict_id_list)).order_by(Dictionary.created_time.desc).all()
#             cat.append(dicts)
#             db.session.add(cat)
#             db.session.commit()
#     elif type == 'unbind' and cat:
#         if isinstance(list, dict_id_list):
#             dicts = Dictionary.query.filter(Dictionary.id.in_(dict_id_list)).order_by(Dictionary.created_time.desc).all()
#             cat.remove(dicts)
#             db.session.add(cat)
#             db.session.commit()
#
#     else:
#         return 'input error'




