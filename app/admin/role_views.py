#encoding: utf-8

from flask import render_template,request,current_app
from datetime import datetime
from flask import redirect,url_for,jsonify
from app.common import logger
from flask_login import login_url,current_user,login_required
from app.common.time_util import *
from sqlalchemy import func

from . import admin
from app.models import User,Action,Role,users_roles,roles_actions

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
    page_size=request.args.get('rows', 5, type=int)
    page=request.args.get('page', 1, type=int)

    pagination = Role.query.order_by(Role.created_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    roles = pagination.items
    prev = None

    if pagination.has_prev:
        prev = url_for('admin.role_list', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('admin.role_list', page=page + 1)
    return jsonify({
        'rows': [role.to_json() for role in roles],
        'prev': prev,
        'next': next,
        'total': pagination.total,
        'time': get_localtime()
    })


@admin.route('/roles/<string:role_id>/actions',methods=['GET'])
def get_actions(role_id):
    actions = Action.query.join(roles_actions).join(Role).filter(Role.id == role_id)
    #actions_count = actions.query(func.count(Role.id)).scalar()

    return jsonify({
        'rows': [action.to_json() for action in actions],
        'total': actions.count(),   #数据量大后，可能是查询慢的一个原因
        'time': get_localtime()
    })







