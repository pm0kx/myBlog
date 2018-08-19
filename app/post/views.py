#encoding: utf-8

from flask import render_template
from flask import redirect,url_for
from flask import session, abort, request
from flask_login import login_required, current_user
#from flask_principal import Permission, UserNeed
from app.common.permission import permission,permission_required
import datetime

from app.post import sidebar_data
from app.models import Post, Comment,User,Tag
from app.common.forms import CommentForm,PostForm
from app.common.extensions import cache
from app.common.db import db
from app.post import post,make_cache_key
# from app.common.extensions import poster_permission, admin_permission

@post.route('/')
@post.route('/<int:page>')
@cache.cached(timeout=60)
def list(page=1):
    """View function for main page"""

    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page, 5)

    # recent, top_tags = sidebar_data()
    return render_template("post/post_home.html",
                           posts=posts)

@post.route('/add',methods=['GET', 'POST'])
@login_required
@permission
def add_post():
    """View function for post page"""

    # Form object: `Post`
    form = PostForm()

    # Ensure the user logged in.
    # Flask-Login.current_user can be access current user.
    if not current_user:
        return redirect(url_for('main.login'))

    if form.validate_on_submit():
        print("submit data:",form.tag.data)
        new_post = Post(title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()
        new_post.tags = db.session.query(Tag).filter_by(id=form.tag.data).all()

        user = db.session.query(User).first()
        new_post.user_id = user.id

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post.list'))

    return render_template('post/add_post.html',form=form)


@post.route('/edit/<string:post_id>',methods=['GET', 'POST'])
@login_required
@permission
def edit_post(post_id):
    """View function for post page"""

    # Form object: `Post`
    post = Post.query.get_or_404(post_id)

    # Ensure the user logged in.
    if not current_user:
        return redirect(url_for('main.login'))

    # Only the post onwer can be edit this post.
    if current_user != post.users:
        return redirect(url_for('post.list'))

    # 当 user 具有编辑权限, 才能够编辑文章
    # permission = Permission(UserNeed(post.users.id))
    # if permission.can() or admin_permission.can():
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.publish_date = datetime.datetime.now()

        # Update the post
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('post.list'))

    form.title.data = post.title
    form.text.data = post.text

    return render_template('post/edit_post.html', form=form, post=post)


@post.route('/detial/<string:post_id>')
def post_detial(post_id):
    """View function for post page"""

    post = Post.query.get_or_404(post_id)

    return render_template('post/post_detial.html',
                           post=post)

#***********************************comment*********************************************

@post.route('/add_comment/<string:post_id>', methods=('GET', 'POST'))
@cache.cached(timeout=60, key_prefix=make_cache_key)
def add_comment(post_id):
    """View function for post page"""

    # Form object: `Comment`
    form = CommentForm()
    # form.validate_on_submit() will be true and return the
    # data object to form instance from user enter,
    # when the HTTP request is POST
    if form.validate_on_submit():
        new_comment = Comment(form.name.data)
        new_comment.text = form.text.data
        new_comment.date = datetime.datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('post.list'))

    post = Post.query.get_or_404(post_id)
    # tags = post.tags
    # comments = post.comments.order_by(Comment.date.desc()).all()

    return render_template('post/add_comment.html',
                           post=post,
                           form=form)



# @post.route('/tag/<string:tag_name>')
# def tag(tag_name):
#     """View function for tag page"""
#
#     tag = db.session.query(Tag).filter_by(name=tag_name).first_or_404()
#     posts = tag.posts.order_by(Post.publish_date.desc()).all()
#     recent, top_tags = sidebar_data()
#
#     return render_template("tag.html",
#                            tag=tag,
#                            posts=posts,
#                            recent=recent,
#                            top_tags=top_tags)

def tag_list():
    pass