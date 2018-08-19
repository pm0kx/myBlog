#encoding: utf-8

from flask import render_template,request,current_app
from datetime import datetime
from flask import redirect,url_for,jsonify
from app.common import logger
from flask_login import login_url,current_user,login_required
from app.common.time_util import *
from sqlalchemy import func

from . import admin
from app.models import User,Action,Resource,Group,Role,users_roles,roles_actions,user_group

logger = logger.Logger(logger="admin-user").getlog()

@admin.route('/get_users',methods=['GET'])
def users_page():
    return render_template("admin/users.html")

@admin.route('/users',methods=['GET'])
#@login_required
def user_list():
    #page = request.args.get('page', 1, type=int)
    page_size=request.args.get('rows', 5, type=int)
    page=request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.created_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    users = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('admin.user_list', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('admin.user_list', page=page + 1)
    return jsonify({
        'rows': [user.to_json() for user in users],
        'prev': prev,
        'next': next,
        'total': pagination.total,
        'time': get_localtime()
    })

@admin.route('/users/<string:user_id>/detial')
def user_detial(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())



@admin.route('/users/<string:user_id>/roles')
def get_roles_by_user(user_id):
    roles = Role.query.join(users_roles).join(User).filter(User.id == user_id)
    return jsonify({
        'rows': [role.to_json() for role in roles],
        'total': roles.count(),
        'time': get_localtime()
    })


@admin.route('/get_groups',methods=['GET'])
def groups_page():
    return render_template("admin/group.html")



@admin.route('/groups',methods=['GET'])
def group_list():
    page_size = request.args.get('rows', 5, type=int)
    page = request.args.get('page', 1, type=int)
    pagination = Group.query.order_by(Group.created_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    groups = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('admin.group_list', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('admin.group_list', page=page + 1)
    return jsonify({
        'rows': [group.to_json() for group in groups],
        'prev': prev,
        'next': next,
        'total': pagination.total,
        'time': get_localtime()
    })


@admin.route('/groups/<string:group_id>/users',methods=['GET'])
def get_user_by_group(group_id):
    users = User.query.join(user_group).join(Group).filter(Group.id == group_id)
    return jsonify({
        'rows': [user.to_json() for user in users],
        'total': users.count(),
        'time': get_localtime()
    })


@admin.route('/groups/add',methods=['POST'])
def add_group():
    data = request.form.to_dict()

    group =Group(data.get('group_name'))
    group.comments =data.get('comments')
    parent_id = data.get('parent_id')
    if parent_id ==None:
        group.parent_id =''
        group.level = 1
    else:
        group.parent_id = parent_id
        parent_group = Group.query.filter(Group.id == parent_id).first()
        group.level = parent_group + 1

    db.session.add(group)
    db.session.commit()

    return jsonify({
        'code': 200,
        'msg': 'ok !'
    })

@admin.route('/groups/<string:group_id>',methods=['PETCH'])
def edit_group(group_id):
    data = request.form.to_dict()
    group = Group.query.filter(Group.id == group_id).first()
    if not group ==None:
        for attr,val in data.items():
            setattr(Group,attr,val)

    parent_id = data.get('parent_id')
    if parent_id == None:
        group.parent_id = ''
        group.level = 1
    else:
        group.parent_id = parent_id
        parent_group = Group.query.filter(Group.id == parent_id).first()
        group.level = parent_group + 1

    db.session.add(group)
    db.session.commit()

    return jsonify({
        'code': 200,
        'msg': 'ok !'
    })

@admin.route('/groups/<string:group_id>',methods=['DELETE'])
def del_group(group_id):
    group = Group.query.filter(Group.id == group_id).first()
    if not group == None:
        db.session.delete(group)
        db.session.commit()
        return jsonify({
            'code': 200,
            'msg': 'ok !'
        })
    else:
        return 'error'

@admin.route('/groups/bind-user/',methods=['POST'])
def bind_user_to_group(user_id):
    data = request.form.to_dict()
    type = data.get('type')
    group_id = data.get('group_id')
    group = Group.query.filter(Group.id == group_id).first()
    user_id_list= data.get('user_id')

    if type =='bind'and group:
        if isinstance(list,user_id_list):
            users = User.query.filter(User.id.in_(user_id_list)).order_by(User.created_time.desc).all()
            group.append(users)
            db.session.add(group)
            db.session.commit()
    elif type =='unbind'and group:
        if isinstance(list,user_id_list):
            users = User.query.filter(User.id.in_(user_id_list)).order_by(User.created_time.desc).all()
            group.remove(users)
            db.session.add(group)
            db.session.commit()

    else:
        return 'input error'


@admin.route('/get_tree',methods=['GET'])
def get_tree():
    return jsonify({
        'time':get_localtime(),
        'data': [
                           {
                            "id": "ajson1",
                            "pid": "0",
                            "name": "Simple root node"
                           },
                           {
                             "id": "ajson2",
                             "pid": "0",
                             "name": "Root node 2"
                            },
                           {
                             "id": "ajson3",
                             "pid": "1",
                             "name": "Child 1"
                            }
                         ]
    })

#
# @admin.route('/groups/bind/<string:user_id>',methods=['DELETE'])
# def unbind_from_group():
#     return ''