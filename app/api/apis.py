#encoding: utf-8

from app.models import Comment
from flask_restful import Resource,reqparse
from app.common.custom_response import ResponseCode,generate_response,ResponseMsg

# from flask_restful import fields, marshal_with

# comment_fields = {
#     'id': fields.String(),
#     'name': fields.String(),
#     'text': fields.String(),
#     'reviewers': fields.String(attribute='creater'),
#     'created_time': fields.String(),
#     'post_title': fields.String(attribute=lambda x: x.posts.title)}


class CommentApi(Resource):

    def __init__(self):
        self.post_get_parser = reqparse.RequestParser()

        self.post_get_parser.add_argument(
            'page',
            type=int,
            location=['json', 'args'],
            required=False)

        self.post_get_parser.add_argument(
            'limit',
            type=int,
            location=['json', 'args'])


    #@marshal_with(comment_fields)
    def get(self, id=None):
        if id:
            comment = Comment.query.get_or_404(id)
            if comment ==None:
                return {'msg':'not exist'},400
            return comment
        else:
            args = self.post_get_parser.parse_args()
            page = args['page'] or 1
            page_size = args['limit'] or 5
            pagination = Comment.query.order_by(Comment.created_time.desc()).paginate(
                page, per_page=page_size, error_out=False)

            return generate_response(data=pagination.items,
                                     count=pagination.total)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
