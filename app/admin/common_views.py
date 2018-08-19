#encoding: utf-8

from flask import render_template,request,current_app
from datetime import datetime
from flask import redirect,url_for,jsonify
from app.common import logger
from flask_login import login_url,current_user,login_required
from app.common.time_util import *
from sqlalchemy import func

from . import admin
from app.models import User,Attachment,Catalog,Dictionary,ActionLog

logger = logger.Logger(logger="admin-common").getlog()

# @admin.route('/get_users',methods=['GET'])
# def users_page():
#     return render_template("admin/users.html")

@admin.route('/catalogs',methods=['GET'])
def catalog_list():
    page_size=request.args.get('rows', 5, type=int)
    page=request.args.get('page', 1, type=int)
    pagination = Catalog.query.order_by(Catalog.created_time.asc()).paginate(
        page, per_page=page_size,
        error_out=False)
    catalogs = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('admin.catalog_list', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('admin.catalog_list', page=page + 1)
    return jsonify({
        'rows': [catalog.to_json() for catalog in catalogs],
        'prev': prev,
        'next': next,
        'total': pagination.total,
        'time': get_localtime()
    })

@admin.route('/catalogs/<string:catalog_id>',methods=['GET'])
def get_catalog(catalog_id):
    catalog = User.query.get_or_404(catalog_id)
    return jsonify(catalog.to_json())



@admin.route('/catalogs/<string:catalog_id>/dictionaries',methods=['GET'])
def get_dictionaries_by_catalog(catalog_id):
    dictionaries = Dictionary.query.filter(Dictionary.catalog_id == catalog_id).first()
    return jsonify({
        'rows': [dictionary.to_json() for dictionary in dictionaries],
        'total': dictionaries.count(),
        'time': get_localtime()
    })


def add_catalog():
    return ''


def edit_catalog(catalog_id):
    return ''


def del_catalog(catalog_id):

    return ''


def add_dictionary():
    return ''


def edit_dictionary(id):
    return ''


def del_dictionary(id):
    return ''


def bind_dictionary_to_catalog():
    return ''




