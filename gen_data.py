#encoding: utf-8

import random
import datetime

from app.common.db import db
from app.models import User, Tag, Post,Role,Action

def gen_randomstr(len):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(len):
        sa.append(random.choice(seed))
    return ''.join(sa)



# user = User.query.filter_by(username='test').first()
# print(user.username)
#--------------------------新增管理员用户-----------------------

def add_user():
    user = User()
    user.username=input('user:')
    user.password=input('passwd:')
    user.address=input('address:')
    user.full_name=input('full_name:')
    user.nick_name=input('nick_name:')
    db.session.add(user)
    db.session.commit()




#--------------------------新增角色数据------------------------------

def add_role():
    name=input('please input username,if default  ,then iput def to skip: ')
    if name == 'def':
        user=db.session.query(User).first()
    else:
        user = User.query.filter_by(username=name).first()
        if not user:
            print('input error')
            return
    role_name=input('role:')
    role_admin = Role(role_name)

    role_admin.users = [user]

    db.session.add(role_admin)

    db.session.commit()


#-------------------------------新增标签--------------------------------

def add_tag():
    tag_one = Tag(name='classic')
    tag_two = Tag(name='faddish')
    tag_three = Tag(name='popular')
    tag_four = Tag(name='diary')

    db.session.add(tag_one)
    db.session.add(tag_two)
    db.session.add(tag_three)
    db.session.add(tag_four)

    db.session.commit()
    
#--------------------------新增标签文章------------------------------

def add_post():
    user1 = db.session.query(User).first()
    
    tags = db.session.query(Tag).filter_by(status=1).all()

    postprefix=input('post prefix:')
    for i in range(10):
        new_post = Post(title=postprefix + str(i))
        new_post.user_id = user1.id
        new_post.publish_date = datetime.datetime.now()
        new_post.text = gen_randomstr(64)
        new_post.tags = random.sample(tags, random.randint(1, 4))
        db.session.add(new_post)

    db.session.commit()

#--------------------------建立用户权限------------------------------

def add_permission():
    name=input('please input role_name,if default  ,then iput def to skip: ')
    if name == 'def':
        role=db.session.query(Role).first()
    else:
        role = Role.query.filter_by(name=name).first()
        if not role:
            print('input error')
            return
    action_name=input('input action name:')
    action=Action(action_name)
    action.code=input('input action code:')
    action.type=input('input action type:')

    role.actions.append(action)
    db.session.add(role)
    db.session.commit()


#------------------------------------------------------------------#

fun={
    'adduser':add_user,
    'addrole':add_role,
    'addtag':add_tag,
    'addpost':add_post,
    'addpermission':add_permission
}

print("add init data")
for i in range(10):
   sel=input('please select action:') 
   if sel =='quit':
        break
   else:
        if sel in fun:
            f=fun.get(sel)
            f()
        else:
            continue



