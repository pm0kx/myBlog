#encoding: utf-8

from flask import request
from datetime import datetime
from flask import jsonify

from app.common import logger
from app.common.time_util import get_localtime
from app.common.action_log import action_log
from app.common.extensions import cache

from app.api import api
from app.models import User,Post,Comment
from app.post import post,make_cache_key
from app.common.db import db


logger = logger.Logger(logger="api-comments").getlog()



@api.route('/comments/', methods=['GET'])
def get_comments():
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.created_time.desc()).paginate(
        page, per_page=page_size,error_out=False)

    comments = pagination.items
    return jsonify({
        'data': [comment.to_json() for comment in comments],
        'msg': '',
        'code': 0,
        'count': pagination.total
    })


@api.route('/comments/<string:id>', methods=['GET'])
def get_comment_by_id(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/posts/<string:id>/comments/')
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    if post ==None:
        return jsonify({
        'code': 1,
        'msg': 'not exist'
        })
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=page_size,error_out=False)
    comments = pagination.items
    return jsonify({
        'data': [comment.to_json() for comment in comments],
        'msg': '',
        'code': 0,
        'count': pagination.total
    })


@api.route('/posts/<string:id>/comments/', methods=['POST'])
def new_post_comment(id):
    post = Post.query.get_or_404(id)
    if post ==None:
        return jsonify({
        'code': 1,
        'msg': 'not exist'
        })
    comment = Comment(request.json.name)
    comment.text =request.json.text
    comment.posts = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json())

def del_comment(id):
    pass

# @post.route('/add_comment/<string:post_id>', methods=('GET', 'POST'))
# @cache.cached(timeout=60, key_prefix=make_cache_key)
# def add_comment(post_id):
#     """View function for post page"""

#     # Form object: `Comment`
#     form = CommentForm()
#     # form.validate_on_submit() will be true and return the
#     # data object to form instance from user enter,
#     # when the HTTP request is POST
#     if form.validate_on_submit():
#         new_comment = Comment(form.name.data)
#         new_comment.text = form.text.data
#         new_comment.date = datetime.datetime.now()
#         new_comment.post_id = post_id
#         db.session.add(new_comment)
#         db.session.commit()
#         return redirect(url_for('post.list'))

#     post = Post.query.get_or_404(post_id)
#     # tags = post.tags
#     # comments = post.comments.order_by(Comment.date.desc()).all()

#     return render_template('post/add_comment.html',
#                            post=post,
#                            form=form)