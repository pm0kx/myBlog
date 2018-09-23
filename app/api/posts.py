#encoding: utf-8

from flask import request
from datetime import datetime
from flask import jsonify
from flask import session, abort
from app.common import logger
from app.common.action_log import action_log
from app.common.extensions import cache
from app.common.permission import permission,permission_required
import json
import re

from app.api import api
from app.models import User,Post,Tag
from app.post import post,make_cache_key
from app.common import utils
from app.common.db import db
#from .errors import forbidden


logger = logger.Logger(logger="api-posts").getlog()


@api.route('/posts/',methods=['GET','POST'])
@cache.cached(timeout=60)
def get_posts():
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)
    if request.method =='GET':
        pagination = Post.query.order_by(Post.publish_date.asc()).paginate(
            page, per_page=page_size,
            error_out=False)
        posts = pagination.items
        return jsonify({
            'data': [post.to_json() for post in posts],
            'msg': '',
            'code': 0,
            'count': pagination.total,
            'time': datetime.now()
        })
    elif request.method =='POST':
        return add_post(request)
    else:
        pass


@api.route('/users/<string:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    if user ==None:
        return jsonify({
        'code': 1,
        'msg': 'not exist'
    })
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.publish_date.desc()).paginate(
        page, per_page=page_size,error_out=False)
    posts = pagination.items

    return jsonify({
        'data': [post.to_json() for post in posts],
        'msg':'',
        'code': 0,
        'count': pagination.total
    })


@api.route('/posts/<string:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_json())


def add_post(request):
    """
    新增post
    :param request:
    :return: json
    """
    data, msg = utils.get_post_data(request)
    post = Post.query.filter_by(title=data['title']).first()

    new_post = Post(data['title'])
    
    new_post.text = data['text']
    new_post.publish_date = datetime.now()

    tag = Tag.query.filter_by(name=data['tag']).first()
    new_post.tags = tag

    user = User.query.get_or_404(data['user_id'])
    new_post.users=user

    db.session.add(new_post)
    db.session.commit()
    return jsonify({
        'code': 0,
        'msg': 'ok'
    })



@api.route('/posts/<string:post_id>',methods=['DELETE', 'PUT'])
def edit_post(post_id):
    """
    修改post
    :param post_id:
    :return: str
    """
    post = Post.query.get_or_404(post_id)
    data, msg = utils.get_post_data(request)
    post.title = data['title']
    post.text = data['text']

    db.session.add(post)
    db.session.commit()

    return jsonify({
        'code': 0,
        'msg': 'ok'
    })

def del_post(post_id,request):
    """
    删除post
    :param post_id:
    :param request:
    :return:json
    """
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()

    return jsonify({
        'code': 0,
        'msg': 'ok'
    })


#@api.route('/tags/<string:id>',methods=['DELETE','PATCH'])
@api.route('/tags',methods=['GET','POST'])
def do_tags():
    resp=None
    if request.method =='GET':
        resp=get_tags(request)
    elif request.method =='POST':
        resp=add_tags(request)
    elif request.method =='PATCH':
        resp =update_tag(id,request)
    return resp

def get_tags(request):
    """
    分页查询tags
    :param request:
    :return:
    """
    page_size = request.args.get('limit', 5, type=int)
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(Tag.created_time.desc()).paginate(
        page, per_page=page_size, error_out=False)
    tags = pagination.items

    return jsonify({
        'data': [tag.to_json() for tag in tags],
        'msg': '',
        'code': 0,
        'count': pagination.total,
        'time': datetime.now()
    })

def add_tags(request):
    """
    新增tags
    :param request:
    :return:
    """
    data,msg=utils.get_post_data(request)
    tag_name= data['tag']
    if tag_name == None:
        return jsonify({
            'msg':'name is required'
        })
    tag = Tag.query.filter_by(name=tag_name).first()
    if tag ==None:
        new_tag = Tag(tag_name)
        new_tag.status = data.get('status')
        new_tag.created_time = datetime.now()
        new_tag.modified_time = datetime.now()
        new_tag.creater = 'lucy'

        db.session.add(new_tag)
        db.session.commit()

    else:
        return jsonify({
            'msg':'tag exist !'
        })
    action_log(request,'添加标签')
    return jsonify({
        'msg':msg,
        'code': 0,
        'time': datetime.now()
        })

@api.route('/tags/<string:id>',methods=['DELETE','PATCH'])
def update_tags(id):
    resp=None
    if request.method=='PATCH':
        resp=update_tag(id,request)
    else:
        resp =del_tag(id,request)
    return resp

def update_tag(id,request):
    """
    更新tag
    :param id:
    :param request:
    :return: json
    """
    data, msg = utils.get_post_data(request)
    #tag_id = request.args.get("id") or None
    if id == None:
        return jsonify({
            'msg': 'tag is not exist'
        })
    tag = Tag.query.filter_by(id=id).first()
    if not tag == None:
        for attr,val in data.items():
            if hasattr(tag,attr) and getattr(tag, "name") !=val:
                setattr(tag, attr, val)
            else:
                return jsonify({
                      'msg': 'tag is exist'
                })
        db.session.add(tag)
        db.session.commit()

    else:
        return jsonify({
            'msg': 'tag is not exist'
        })
    action_log(request, '修改标签')
    return jsonify({
        'msg': msg,
        'code': 0,
        'time': datetime.now()
    })

def del_tag(id,request):
    """
    删除tag
    :param id:
    :param request:
    :return:
    """
    if id == None:
        return jsonify({
            'msg': 'tag is not exist'
        })
    tag = Tag.query.filter_by(id=id).first()
    if not tag == None:
        db.session.delete(tag)
        db.session.commit()
    else:
        return jsonify({
            'msg': 'tag is not exist'
        })
    action_log(request, '删除标签')
    return jsonify({
        'msg': 'ok',
        'code': 0,
        'time': datetime.now()
    })


@api.route('/post/test',methods=['POST'])
def test_posts():
    tb,msg=utils.get_post_data(request)
    return jsonify({
            'msg':msg,
            'data':tb
        })



@api.route('/tags/<string:id>/change-status')
def change_tag_status(id):
    if not utils.check_str(id):
        return jsonify({
            'msg': 'id is illegal'
        })
    tag = Tag.query.filter_by(id=id).first()
    status =request.args.get('status')
    if not tag == None:
        tag.status=status
        db.session.add(tag)
        db.session.commit()
    else:
        return jsonify({
            'msg': 'tag is not exist'
        })
    action_log(request, '更改标签状态')
    return jsonify({
        'msg': 'ok',
        'code': 0,
        'time': datetime.now()
    })

@api.route('/posts/<string:id>/change-status')
def change_post_status(id):
    if not utils.check_str(id):
        return jsonify({
            'msg': 'id is illegal'
        })
    post = Post.query.filter_by(id=id).first()
    status =request.args.get('status')
    if not post == None:
        post.status=status
        db.session.add(post)
        db.session.commit()
    else:
        return jsonify({
            'msg': 'post is not exist'
        })
    action_log(request, '更改文章状态')
    return jsonify({
        'msg': 'ok',
        'code': 0,
        'time': datetime.now()
    })