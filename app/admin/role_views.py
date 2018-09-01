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
from app.models import User,Action,Role,users_roles,roles_actions,Resource

logger = logger.Logger(logger="admin-api").getlog()



@admin.route('/roles/<string:role_id>/users',methods=['GET'])
def get_users_by_role(role_id):
    users = User.query.join(users_roles).join(Role).filter(Role.id == role_id)
    return jsonify({
        'rows': [user.to_json() for user in users],
        'total': users.count(),
        'time': get_localtime()
    })


@admin.route('/get_roles',methods=['GET'])
def roles_page():
    return render_template("admin/roles.html")


@admin.route('/roles',methods=['GET'])
def role_list():
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)

    pagination = Role.query.order_by(Role.created_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    roles = pagination.items
    # prev = None
    # if pagination.has_prev:
    #     prev = url_for('admin.role_list', page=page - 1)
    # next = None
    # if pagination.has_next:
    #     next = url_for('admin.role_list', page=page + 1)
    return jsonify({
        'data': [role.to_json() for role in roles],
        'msg': '',
        'code': 0,
        'count': pagination.total,
        'time': get_localtime()
    })

@admin.route('/roles',methods=['POST'])
def add_role():
    data = request.form.to_dict()
    role_name = data.get('name')
    role = Role.query.filter_by(name=role_name).first()
    if role == None:
        role_new = Role(role_name)
        role_new.description = data.get('description')
        role_new.created_time = datetime.now()
        db.session.add(role_new)
        db.session.commit()
    else:
        return jsonify({
            'msg': 'role name exist !'
        })
    action_log(request, '添加角色')
    return jsonify({
        'msg': 'ok !'
    })


@admin.route('/roles',methods=['PUT'])
def edit_role():
    data = request.form.to_dict()
    role_id = data.get('id')
    role_name = data.get('name')
    role = Role.query.filter_by(id=role_id).first()
    if not role == None:
        if not role_name ==None:
            role.name = role_name
        role.description = data.get('description')
        role.modified_time = datetime.now()
        db.session.add(role)
        db.session.commit()
    else:
        return jsonify({
            'msg': 'role not exist !'
        })
    action_log(request, '修改角色')
    return jsonify({
        'msg': 'ok !'
    })

@admin.route('/roles/<string:role_id>',methods=['DELETE'])
def del_role(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if not role == None:
        db.session.delete(role)
        db.session.commit()
    else:
        return jsonify({
            'msg': 'role not exist !'
        })
    action_log(request, '删除角色')
    response =jsonify({'msg': 'ok !' })
    response.status_code = 200
    return response

@admin.route('/roles/<string:role_id>/actions',methods=['GET'])
def get_actions(role_id):
    actions = Action.query.join(roles_actions).join(Role).filter(Role.id == role_id)
    #actions_count = actions.query(func.count(Role.id)).scalar()

    return jsonify({
        'rows': [action.to_json() for action in actions],
        'total': actions.count(),   #数据量大后，可能是查询慢的一个原因
        'time': get_localtime()
    })



@admin.route('/roles/bind-action/',methods=['POST'])
def bind_action_to_role():
    data = request.form.to_dict()
    role_id = data.get('role_id')
    role = Role.query.filter_by(id=role_id).first()
    action_list= data.get('action_id')

    if  role:
        if isinstance(list,action_list):
            role.actions.clear()
            actions = Action.query.filter(Action.id.in_(action_list)).order_by(Action.created_time.desc).all()
            role.actions.extend(actions)
            db.session.add(role)
            db.session.commit()

    else:
        return 'input error'


@admin.route('/roles/bind-resource/',methods=['POST'])
def bind_res_to_role():
    data = request.form.to_dict()
    role_id = data.get('role_id')
    role = Role.query.filter_by(id=role_id).first()
    res_list = data.get('resource_id')

    if role:
        if isinstance(list, res_list):
            role.resources.clear()
            res = Resource.query.filter(Resource.id.in_(res_list)).order_by(Resource.created_time.desc).all()
            role.resources.extend(res)
            db.session.add(role)
            db.session.commit()

    else:
        return 'input error'


