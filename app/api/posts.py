#encoding: utf-8

from flask import request
from datetime import datetime
from flask import jsonify
from flask import session, abort
from app.common import logger
from app.common.action_log import action_log
from app.common.extensions import cache
from app.common.permission import permission,permission_required

from app.api import api
from app.models import User,Post,Tag
from app.post import post,make_cache_key
from app.common.db import db
#from .errors import forbidden


logger = logger.Logger(logger="api-posts").getlog()

					   

@api.route('/posts/',methods=['GET'])
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
        pass
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




@api.route('/tags',methods=['GET'])
def get_tags():
    #tags = Tag.query.filter_by(status=1).all()
    
    page_size=request.args.get('limit', 5, type=int)
    page=request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(Tag.created_time.desc()).paginate(
        page, per_page=page_size,error_out=False)
    tags = pagination.items

    return jsonify({
        'data': [tag.to_json() for tag in tags],
        'msg':'',
        'code': 0,
        'count': pagination.total,
        'time': datetime.now()
    })



# @post.route('/add',methods=['GET', 'POST'])
# @login_required
# @permission
# def add_post():
#     """View function for post page"""

    # Form object: `Post`
    # form = PostForm()

    # Ensure the user logged in.
    # Flask-Login.current_user can be access current user.
    # if not current_user:
    #     return redirect(url_for('main.login'))

    # if form.validate_on_submit():
    #     print("submit data:",form.tag.data)
    #     new_post = Post(title=form.title.data)
    #     new_post.text = form.text.data
    #     new_post.publish_date = datetime.datetime.now()
    #     new_post.tags = db.session.query(Tag).filter_by(id=form.tag.data).all()

    #     user = db.session.query(User).first()
    #     new_post.user_id = user.id

    #     db.session.add(new_post)
    #     db.session.commit()
    #     return redirect(url_for('post.list'))

    # return render_template('post/add_post.html',form=form)


# @post.route('/edit/<string:post_id>',methods=['GET', 'POST'])
# @login_required
# @permission
# def edit_post(post_id):
#     """View function for post page"""

#     # Form object: `Post`
#     post = Post.query.get_or_404(post_id)

#     # Ensure the user logged in.
#     if not current_user:
#         return redirect(url_for('main.login'))

#     # Only the post onwer can be edit this post.
#     if current_user != post.users:
#         return redirect(url_for('post.list'))

    # 当 user 具有编辑权限, 才能够编辑文章
    # permission = Permission(UserNeed(post.users.id))
    # if permission.can() or admin_permission.can():
    # form = PostForm()
    # if form.validate_on_submit():
    #     post.title = form.title.data
    #     post.text = form.text.data
    #     post.publish_date = datetime.datetime.now()

    #     # Update the post
    #     db.session.add(post)
    #     db.session.commit()

    #     return redirect(url_for('post.list'))

    # form.title.data = post.title
    # form.text.data = post.text

    # return render_template('post/edit_post.html', form=form, post=post)




# @api.route('/users/<int:id>/timeline/')
# def get_user_followed_posts(id):
#     user = User.query.get_or_404(id)
#     page = request.args.get('page', 1, type=int)
#     pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     prev = None
#     if pagination.has_prev:
#         prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
#     next = None
#     if pagination.has_next:
#         next = url_for('api.get_user_followed_posts', id=id, page=page+1)
#     return jsonify({
#         'posts': [post.to_json() for post in posts],
#         'prev': prev,
#         'next': next,
#         'count': pagination.total
#     })
	
	
	
	
	
	


