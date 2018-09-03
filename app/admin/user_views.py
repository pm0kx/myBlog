#encoding: utf-8

from flask import render_template,request,current_app
from datetime import datetime
from flask import redirect,url_for,jsonify
from app.common import logger
from flask_login import login_url,current_user,login_required
from app.common.time_util import *
from app.common.action_log import action_log
from sqlalchemy import func

from . import admin
from app.models import User,Mail,Group,Role,users_roles,user_group

logger = logger.Logger(logger="admin-user").getlog()

@admin.route('/get_users',methods=['GET'])
def users_page():
    return render_template("admin/users.html")

@admin.route('/users',methods=['GET'])
#@login_required
def user_list():
    #page = request.args.get('page', 1, type=int)
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)
    type=request.args.get('type')
    if type ==None:
        pagination = User.query.filter(User.type == '1').order_by(User.created_time.asc()).paginate(
            page, per_page=page_size,
            error_out=False)
    else:
        #pagination = User.query.join(user_group).join(Group).filter(Group.group_name == group_name) \
        pagination = User.query.filter(User.type == type).order_by(User.created_time.asc()).paginate(
            page, per_page=page_size,
            error_out=False)
    users = pagination.items

    # prev = None
    # if pagination.has_prev:
    #     prev = url_for('admin.user_list', page=page - 1)
    # next = None
    # if pagination.has_next:
    #     next = url_for('admin.user_list', page=page + 1)
    return jsonify({
        'data': [user.to_json() for user in users],
        'msg': '',
        'code': 0,
        'count': pagination.total,
        'time': get_localtime()
    })

@admin.route('/users/<string:user_id>',methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())



@admin.route('/users',methods=['POST'])
def add_user():
    data = request.form.to_dict()
    user = User.query.filter_by(username=data.get('username')).first()
    if user ==None:
        new_user = User()
        new_user.username = data.get('username')
        new_user.password = 'abcd1234'  # default password
        new_user.nick_name = data.get('nick_name')
        new_user.full_name = data.get('full_name')
        new_user.address = data.get('address')
        new_user.birthday = data.get('birthday')
        new_user.gender = data.get('gender')
        new_user.status = 1  # 0：禁用，1：启用
        new_user.confirmed = True  # 未确认

        mail = Mail(data.get('mail'))
        mail.user_id = new_user.id
        mail.status = 1

        db.session.add(new_user)
        db.session.add(mail)
        db.session.commit()

    else:
        return jsonify({
            'msg':'username exist !'
        })
    action_log(request,'添加用户')
    return jsonify({
            'msg':'ok !'
        })


@admin.route('/users',methods=['PUT'])
def edit_user():
    data = request.form.to_dict()
    user = User.query.filter_by(id=data.get('id')).first()
    is_update = False
    if not user == None:
        for attr, val in data.items():
            if hasattr(User, attr):  # 检查实例是否有这个属性
                if attr =='username':
                    logger.info("用户名不支持修改！")
                    continue
                if not val ==None:
                    setattr(User, attr, val)  # same as: a.name =
                    is_update = True
        if is_update:
            user.modified_time =datetime.now()
            db.session.add(user)
            db.session.commit()
    else:
        return jsonify({
            'msg': 'user not exist !'
        })
    action_log(request, '修改用户信息')
    return jsonify({
        'msg': 'ok !'
    })

@admin.route('/users/<string:user_id>',methods=['DELETE'])
def del_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user == None:
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'msg': 'ok !'
        })
    else:
        return 'error'



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
    page_size = request.args.get('limit', 5, type=int)
    page = request.args.get('page', 1, type=int)
    pagination = Group.query.order_by(Group.created_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    groups = pagination.items

    # prev = None
    # if pagination.has_prev:
    #     prev = url_for('admin.group_list', page=page - 1)
    # next = None
    # if pagination.has_next:
    #     next = url_for('admin.group_list', page=page + 1)
    return jsonify({
        'data': [group.to_json() for group in groups],
        'msg': '',
        'code': 0,
        'count': pagination.total,
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
        'msg': 'ok !'
    })

@admin.route('/groups/<string:group_id>',methods=['DELETE'])
def del_group(group_id):
    group = Group.query.filter(Group.id == group_id).first()
    if not group == None:
        db.session.delete(group)
        db.session.commit()
        return jsonify({
            'msg': 'ok !'
        })
    else:
        return 'error'

@admin.route('/groups/bind-user/',methods=['POST'])
def bind_user_to_group():
    data = request.form.to_dict()
    group_id = data.get('group_id')
    group = Group.query.filter(Group.id == group_id).first()
    user_id_list= data.get('user_id')

    if type =='bind'and group:
        if isinstance(list,user_id_list):
            group.users.clear()
            users = User.query.filter(User.id.in_(user_id_list)).order_by(User.created_time.desc).all()
            for u in users:
                group.users.append(u)
            db.session.add(group)
            db.session.commit()
    else:
        return 'input error'

# @admin.route('/groups/bind-user/',methods=['POST'])
# def bind_user_to_group(user_id):
#     data = request.form.to_dict()
#     type = data.get('type')
#     group_id = data.get('group_id')
#     group = Group.query.filter(Group.id == group_id).first()
#     user_id_list= data.get('user_id')
#
#     if type =='bind'and group:
#         if isinstance(list,user_id_list):
#             users = User.query.filter(User.id.in_(user_id_list)).order_by(User.created_time.desc).all()
#             group.users.append(users)
#             db.session.add(group)
#             db.session.commit()
#     elif type =='unbind'and group:
#         if isinstance(list,user_id_list):
#             users = User.query.filter(User.id.in_(user_id_list)).order_by(User.created_time.desc).all()
#             group.users.remove(users)
#             db.session.add(group)
#             db.session.commit()
#
#     else:
#         return 'input error'


@admin.route('/users/bind-role/',methods=['POST'])
def bind_user_to_role():
    data = request.form.to_dict()
    user_id = data.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    roleid_list= data.get('role_id')

    if  user:
        if isinstance(list,roleid_list):
            user.roles.clear()
            roles = Role.query.filter(Role.id.in_(roleid_list)).order_by(Role.created_time.desc).all()
            user.roles.extend(roles)
            db.session.add(user)
            db.session.commit()

    else:
        return 'input error'

def add_role_to_user(ids):
    obj =[]
    for id in ids:
        role =  Role.query.filter(Role.id == id)
        if not role ==None:
            obj.append(role)
    return obj

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

@admin.route('/json',methods=['GET'])
def get_json():
     
    return jsonify({
    "code": 0,
    "msg": "",
    "count": "12",
    "data": [
    {
    "id": "001",
    "label": "美食",
    "title": "舌尖上的中国第一季",
    "author": "作者-1",
    "content": "通过中华美食的多个侧面，来展现食物给中国人生活带来的仪式、",
    "uploadtime": 20121204,
    "status": True
  },
  {
    "id": "002",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": False
  },
  {
    "id": "003",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": True
  },
  {
    "id": "004",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": False
  },
  {
    "id": "005",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": True
  },
  {
    "id": "006",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": True
  },
  {
    "id": "007",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": True
  },
  {
    "id": "00,8",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": False
  },
  {
    "id": "009",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": False
  },
  {
    "id": "010",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": False
  },
  {
    "id": "011",
    "label": "体育",
    "title": "舌尖上的中国第二季",
    "author": "作者-2",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": False
  },
  {
    "id": "012",
    "label": "美食",
    "title": "舌尖上的中国第二季",
    "author": "作者-12",
    "content": "以食物为窗口，读懂中国——通过美食，使人们可以有滋有味地认知这个古老的东方国度。",
    "uploadtime": 20141204,
    "status": True
  }
  ]
})
    #resp = jsonify({})
    # resp.status_code = 200
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    # return resp


