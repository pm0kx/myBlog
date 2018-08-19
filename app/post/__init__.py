#encoding: utf-8

from flask import Blueprint,request

post = Blueprint('post',__name__)


#siderbar
from sqlalchemy import func

from app.models import Post, Tag, posts_tags
from app import db
from app import cache

@cache.cached(timeout=7200, key_prefix='sidebar_data')
def sidebar_data():

    """Set the sidebar function."""
    #定义右侧边栏的视图函数

    # Get post of recent
    recent = db.session.query(Post).order_by(
            Post.publish_date.desc()
        ).limit(5).all()

    # Get the tags and sort by count of posts.
    top_tags = db.session.query(
            Tag, func.count(posts_tags.c.post_id).label('total')
        ).join(
            posts_tags
        ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags


def make_cache_key(*args, **kwargs):
    """Dynamic creation the request url."""

    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode('utf-8')

from . import views