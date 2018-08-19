#encoding: utf-8

from flask import Blueprint


admin = Blueprint('admin','__name__')

from . import user_views,action_views,role_views,common_views