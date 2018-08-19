from flask import jsonify, request
from flask import url_for

from app.models import Post,Tag
from app import db
from app.api import api
# from .decorators import permission_required
from .errors import forbidden


@api.route('/posts/',methods=['GET', 'POST'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=5,
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'total': pagination.total
    })


    #  posts = Post.query.order_by(
    #     Post.publish_date.desc()
    # ).paginate(page, 5)

    # recent, top_tags = sidebar_data()

    # return render_template("post/post_home.html",
    #                        posts=posts,
    #                        recent=recent)




@api.route('/posts/<string:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_json())


@api.route('/tag')
def get_tags():
    tags = db.session.query(Tag).filter_by(status=1).all()
    return jsonify({
        'tags': [tag.to_json() for tag in tags],
        'total': len(tags)
    })