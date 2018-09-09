#encoding: utf-8

from uuid import uuid4
import os
from flask import current_app, request, url_for
from flask_login import AnonymousUserMixin,UserMixin
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.common.db import db
from app.common.extensions import bcrypt
from app.common.time_util import format_date



posts_tags = db.Table('posts_tags',
    db.Column('id',db.Integer,primary_key=True,autoincrement=True),
    db.Column('post_id', db.String(45), db.ForeignKey('posts.id')),
    db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')),
    db.Column('status', db.Integer))


users_roles = db.Table('users_roles',
    db.Column('id',db.Integer,primary_key=True,autoincrement=True),
    db.Column('user_id', db.String(45), db.ForeignKey('users.id')),
    db.Column('role_id', db.String(45), db.ForeignKey('roles.id')),
    db.Column('status', db.Integer))

roles_actions = db.Table('roles_actions', # 用户权限关联表
    db.Column('id',db.Integer,primary_key=True,autoincrement=True),
    db.Column('action_id', db.String(45), db.ForeignKey('actions.id')),
    db.Column('role_id', db.String(45), db.ForeignKey('roles.id')),
    db.Column('status', db.Integer))


roles_resources = db.Table('roles_resources',  # 用户菜单关联表
    db.Column('id',db.Integer,primary_key=True,autoincrement=True),
    db.Column('role_id', db.String(45), db.ForeignKey('roles.id')),
    db.Column('resource_id', db.String(45), db.ForeignKey('resources.id')),
    db.Column('status', db.Integer))

user_group = db.Table('user_group',  # 用户机构关联表
    db.Column('id',db.Integer,primary_key=True,autoincrement=True),
    db.Column('user_id', db.String(45), db.ForeignKey('users.id')),
    db.Column('group_id', db.String(45), db.ForeignKey('group.id')),
    db.Column('status', db.Integer))

class BaseModel(object):
    """Base class"""
    # 1:enabled     0:disenabled
    status_ = db.Column(db.Integer,default=1,comment='状态，1->启用，0->禁用')
    created_time = db.Column(db.DATETIME, default=datetime.datetime.now(),comment='创建时间')
    creater = db.Column(db.String(45),default='null')
    modified_time = db.Column(db.DATETIME, default=datetime.datetime.now(), onupdate=datetime.datetime.now(),comment='修改时间')
    modifier = db.Column(db.String(45),default='null')

    def add_or_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def status(self):
        return self.status_

    @status.setter
    def status(self, s):
        if s in [0,1]:
            self.status_=s
        else:
            raise AttributeError('status in [0,1]')

# class Admins(BaseModel,db.Model):
#     pass


class User(BaseModel,db.Model):
    """Represents Proected users."""

    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password_hash = db.Column(db.String(64), comment='加密密文')
    nick_name = db.Column(db.String(64))
    full_name = db.Column(db.String(64))
    type = db.Column(db.String(10), comment='0:administrators,1:member,2:vip')
    gender = db.Column(db.String(10), comment='1:man,0:women')
    birthday = db.Column(db.DateTime)
    address = db.Column(db.Text())
    confirmed = db.Column(db.Integer, default=False,comment='状态，True->已确认，False->未确认')
    # Establish contact with Post's ForeignKey: user_id
    posts = db.relationship(
        'Post',
        backref='users',
        lazy='dynamic')

    roles = db.relationship(
        'Role',
        secondary=users_roles,
        backref=db.backref('users', lazy='dynamic')
        #lazy = 'dynamic',
        # cascade = 'all, delete-orphan',
        # passive_deletes = True
       )

    mails = db.relationship(
        'Mail',
        backref='users',
        lazy='dynamic')

    def __init__(self):
        self.id = str(uuid4())


    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Convert the password to cryptograph via flask-bcrypt"""
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @property
    def actions(self):
        """获取该用户所有的操作权限"""
        actions = Action.query.join(roles_actions).join(Role).join(users_roles).join(User).\
            filter(User.id == self.id)
        return actions


    @property
    def resources(self):
        """获取该用户所有的菜单权限"""
        resources = Resource.query.join(roles_resources).join(Role).join(users_roles).join(User).\
            filter(User.id == self.id).order_by(Resource.order).all()
        return resources


    def check(self,type,action):

        # actions = self.actions.filter(Action.code == action).first()
        return self.roles is not None and self.actions.filter(Action.code == action,Action.type == type).first()

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'avatar': 'http://127.0.0.1:8089/static/images/user/p1.jpg',
            'nick_name': self.nick_name,
            'full_name': self.full_name,
            'birthday': self.birthday,
            'address': self.address,
            'status': self.status,
            'gender': self.gender,
            'create_time': self.created_time,
            'emails': [mail.email for mail in self.mails]
           # 'email':','.join(self.mails.email)
        }
        return json_user
    @property
    def is_authenticated(self):
        """Check the user whether logged in."""

        # Check the User's instance whether Class AnonymousUserMixin's instance.
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
    @property
    def is_active(self):
        """Check the user whether pass the activation process."""

        return True

    @property
    def is_anonymous(self):
        """Check the user's login status whether is anonymous."""

        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        """Get the user's uuid from database."""

        return self.id


class Role(BaseModel,db.Model):
    """Represents Proected roles."""
    __tablename__ = 'roles'

    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    actions = db.relationship(
        'Action',
        secondary=roles_actions,
        backref=db.backref('roles', lazy='dynamic'))


    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name

    def has_permission(self, perm):
        # return self.permissions & perm == perm
        pass

    def to_json(self):
        json_post = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'create_time': self.created_time,
            'update_time': self.modified_time
        }
        return json_post

    def __repr__(self):
        return "<Model Role `{}`>".format(self.name)


class Post(BaseModel,db.Model):
    """Represents Proected posts."""

    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # Set the foreign key for Post
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
    # Establish contact with Comment's ForeignKey: post_id
    comments = db.relationship(
        'Comment',
        backref='posts',
        lazy='dynamic')
    # many to many: posts <==> tags
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,
        backref=db.backref('posts', lazy='dynamic'))
    

    def __init__(self, title):
        self.id = str(uuid4())
        self.title = title

    def get_tag(self):
        tags =Tag.query.join(posts_tags).join(Post).filter(Post.id==self.id)
        str =[]
        for t in tags:
            str.append(t.name)
        return ','.join(str)
    
    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)

    def to_json(self):
        json_post = {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'publish_date': self.publish_date,
            'author': self.users.username,
            'tag':self.get_tag(),
            'status': self.status,
            'created_time': self.created_time
        }
        return json_post



class Comment(BaseModel,db.Model):
    """Represents Proected comments."""

    __tablename__ = 'comments'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self, name):
        self.name = name
        self.id=str(uuid4())
    
    def to_json(self):
        json_comment = {
            'id': self.id,
            'name': self.name,
            'content': self.text,
            'reviewers':self.creater,
            'status': self.status,
            'post_title': self.posts.title,
            'date': self.date,
            'create_time': self.created_time
        }
        return json_comment


    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)



class Tag(BaseModel,db.Model):
    """Represents Proected tags."""

    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self,name):
        self.id = str(uuid4())
        self.name = name

    def to_json(self):
        json_tag = {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'update_time': self.modified_time,
            'create_time': self.created_time
        }
        return json_tag


    def __repr__(self):
        return "<Model Tag `{}`>".format(self.name)

class Catalog(BaseModel,db.Model):
    """dictionary catalog"""

    __tablename__='catalog'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(40),nullable=False,unique=True)
    code = db.Column(db.String(45),unique=True)
    is_show = db.Column(db.String(32))
    comments = db.Column(db.String(255))

    dictionaries=db.relationship(
        'Dictionary',
        backref='catalog')

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return 'Catalog'
    
    def to_json(self):
        json_post = {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'is_show': self.is_show,
            'comments':self.comments,
            'status': self.status,
            'create_time': self.created_time,
            'update_time': self.modified_time
        }
        return json_post



class Dictionary(BaseModel,db.Model):
    """dictionary detail"""

    __tablename__='dictionary'
    id=db.Column(db.String(45),primary_key=True)
    name=db.Column(db.String(100))
    code = db.Column(db.String(45),unique=True)
    order=db.Column(db.Integer)
    catalog_id=db.Column(db.Integer,db.ForeignKey('catalog.id'))

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return 'dict'

    def to_json(self):
        json_post = {
            'id': self.id,
            'name': self.name,
            'order': self.order,
            'code': self.code,
            'status': self.status,
            'create_time': self.created_time,
            'update_time': self.modified_time
        }
        return json_post



class Mail(BaseModel,db.Model):
    """Represents Proected reminders."""

    __tablename__ = 'mails'
    id = db.Column(db.String(45), primary_key=True)
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
    #date = db.Column(db.DateTime())
    email = db.Column(db.String(255))
    text = db.Column(db.Text())

    def __init__(self, text):
        self.id = str(uuid4())
        self.email = text

    def __repr__(self):
        return '<Model Mail `{}`>'.format(self.text[:20])


class Action(BaseModel,db.Model):
    """权限表"""

    __tablename__ = 'actions'
    id = db.Column(db.String(45), primary_key=True)
    #source_id = db.Column(db.String(45), db.ForeignKey('sources.id'))
    name = db.Column(db.String(128))
    type = db.Column(db.String(32))
    code = db.Column(db.String(45),unique=True)
    comments = db.Column(db.String(255))


    def __init__(self, action_name):
        self.id = str(uuid4())
        self.name = action_name

    def to_json(self):
        json_post = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'code': self.code,
            'comments':self.comments,
            'status': self.status,
            'create_time': self.created_time
        }
        return json_post


class Resource(BaseModel,db.Model):
    """菜单资源表"""

    __tablename__ = 'resources'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(128))
    pid = db.Column(db.String(45))
    icon = db.Column(db.String(50))
    url = db.Column(db.String(250))
    order = db.Column(db.SmallInteger, default=0)
    bg_color = db.Column(db.String(50))
    comments = db.Column(db.String(255))

    roles = db.relationship(
        'Role',
        secondary=roles_resources,
        backref=db.backref('resources', lazy='dynamic'))

    def __init__(self, source_name):
        self.id = str(uuid4())
        self.source_name = source_name

    def to_json(self):
        json_post = {
            'id': self.id,
            'name': self.name,
            'pid': self.pid,
            'icon': self.icon,
            'url':self.url,
            'order':self.order,
            'bg_color':self.bg_color,
            'comments':self.comments,
            'status': self.status,
            'create_time': self.created_time
        }
        return json_post

class Group(BaseModel,db.Model):
    """用户组"""

    __tablename__ = 'group'
    id = db.Column(db.String(45), primary_key=True)
    group_name = db.Column(db.String(64))
    parent_id = db.Column(db.String(45))
    level_no =db.Column(db.Integer)        #最大支持3级
    comments = db.Column(db.String(255))

    users = db.relationship(
        'User',
        secondary=user_group,
        backref=db.backref('group', lazy='dynamic'))

    def __init__(self, group_name):
        self.id = str(uuid4())
        self.group_name = group_name

    @property
    def level(self):
        return self.level_no

    @level.setter
    def level(self, num):
        if num.isdigit() and num >0 and  num <=3:
            self.level_no =num
        else:
            raise AttributeError('level错误，level范围为1-3')


    def to_json(self):
        json_post = {
            'id': self.id,
            'group_name': self.group_name,
            'parent_id': self.parent_id,
            'level': self.level,
            'comments':self.comments,
            'status': self.status,
            'create_time': self.created_time
        }
        return json_post

class ActionLog(db.Model):
    """操作日志"""

    __tablename__ = 'action_log'
    id = db.Column(db.String(45), primary_key=True)
    action_name = db.Column(db.String(128))
    client_ip = db.Column(db.String(128))
    action_time = db.Column(db.DateTime())

    def __init__(self, action_name):
        self.id = str(uuid4())
        self.action_name = action_name

    def to_json(self):
        json_post = {
            'id': self.id,
            'action_name': self.action_name,
            'client_ip': self.client_ip,
            'action_time': self.action_time
        }
        return json_post

class Attachment(db.Model):
    """附件资源表"""

    __tablename__ = 'attachments'
    id = db.Column(db.String(45), primary_key=True)
    attach_name = db.Column(db.String(255))
    path = db.Column(db.Text())
    belong_type= db.Column(db.String(45))
    belong_id = db.Column(db.String(45))

    def __init__(self):
        self.id = str(uuid4())

