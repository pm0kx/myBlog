#encoding: utf-8

from flask import render_template,request,current_app
from datetime import datetime
from flask import redirect,url_for,jsonify,json
from app.common import logger
from flask_login import login_url,current_user,login_required
from app.common.time_util import get_localtime
from sqlalchemy import func

from . import admin
from app.models import User,Action,ActionLog,roles_actions,Role,Resource,roles_resources
from app.common.db import db

logger = logger.Logger(logger="admin-api").getlog()


@admin.route('/get_actions',methods=['GET'])
def actions_page():
    return render_template("admin/actions.html")


@admin.route('/actions',methods=['GET'])
def action_list():
    page_size=request.args.get('rows', 5, type=int)
    page=request.args.get('page', 1, type=int)

    pagination = Action.query.order_by(Action.created_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    actions = pagination.items
    prev = None

    if pagination.has_prev:
        prev = url_for('admin.action_list', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('admin.action_list', page=page + 1)
    return jsonify({
        'rows': [action.to_json() for action in actions],
        'prev': prev,
        'next': next,
        'total': pagination.total,
        'time': get_localtime()
    })

@admin.route('/actions/add',methods=['POST'])
def add_action():
    #data = json.loads(request.form)
    data=request.form.to_dict()
    code=data.get('action_code')
    has_action = Action.query.filter(Action.code == code).first()
    if has_action ==None:
        action1=Action(data.get('action_name'))
        action1.type=data.get('action_type')
        action1.code=code
        action1.comments=data.get('action_comments')
        db.session.add(action1)
        db.session.commit()
    else:
        return jsonify({
            'code':500,
            'msg':'action code exist !'
        })
    
    return jsonify({
            'code':200,
            'msg':'sbumit success !'
        })


@admin.route('/actions/<string:action_id>',methods=['PETCH'])
def edit_action(action_id):
    action_new=Action.query.filter(Action.id == action_id).first()
    data = request.form.to_dict()
    is_update = False
    if not action_new == None:
        #更新方法
        #user = db.session.query(User).update({'username': 'update_fanguiju'})
        #db.session.commit()
        for attr, val in data.items():
            if hasattr(Action, attr):  # 检查实例是否有这个属性
                setattr(Action, attr, val)  # same as: a.name =
                is_update = True
        if is_update:
            db.session.add(action_new)
            db.session.commit()
    else:
        return 'error'
    return jsonify({
        'code': 200,
        'msg': 'ok !'
    })



@admin.route('/actions/<string:action_id>',methods=['DELETE'])
def del_action(action_id):
    has_action = Action.query.filter(Action.id == action_id).first()
    if not has_action == None:
        db.session.delete(has_action)
        db.session.commit()
    else:
        return 'error'
    return jsonify({
        'code': 200,
        'msg': 'ok !'
    })

@admin.route('/actions/batch/<string:ids>',methods=['DELETE'])
def del_actions(ids):
    action_ids=ids.spilt(',')
    error_str=''
    for id in action_ids:
        action = Action.query.filter(Action.id == id).first()
        if not action ==None:
            db.session.delete(action)
        else:
            error_str=','.join(id)
    db.session.commit()
    if not error_str ==None:
        return jsonify({
            'code': 200,
            'msg': error_str+" delete fail"
        })


def action_log():
    pass



def resource_list():
    pass
