# -*- coding: UTF-8 -*-
import re
import json
from bson import ObjectId
from datetime import datetime, timedelta

def utc2local(utc_st):
    now_stamp = datetime.now().timestamp()
    local_time = datetime.fromtimestamp(now_stamp)
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st

def get_post_data(request):

    strs=''
    content_type_table =['application/json','application/x-www-form-urlencoded']
    content_type=request.headers.get("Content-Type")

    if content_type not in content_type_table:
        strs='An alternative way of submitting data'

    if content_type ==content_type_table[0]:
        return request.json,strs
    elif content_type ==content_type_table[1]:
        return request.form.to_dict(),strs   
    else:
        return request.form.to_dict(),strs

def get_args_data(request):

    return request.args

def check_str(strs):
    pattern_str='\w|-'
    return re.match(pattern_str, strs, flags=0)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# def verify_num(code):
#     from .code_msg import VERIFY_CODE_ERROR
#
#     if code != session['ver_code']:
#         raise models.GlobalApiException(VERIFY_CODE_ERROR)
#     # return result


# def gen_verify_num():
#     a = random.randint(-20, 20)
#     b = random.randint(0, 50)
#     data = {'question': str(a) + ' + ' + str(b) + " = ?", 'answer': str(a + b)}
#     session['ver_code'] = data['answer']
#     return data


# def gen_cache_key():
#     return 'view//' + request.full_path
#
#
# def send_mail_async(app, msg):
#     with app.app_context():
#         extensions.mail.send(msg)
#
#
# def send_email(to, subject, body, is_txt=True):
#     app = current_app._get_current_object()
#     msg = Message(subject=app.config.get('MAIL_SUBJECT_PREFIX') + subject, sender=app.config.get('MAIL_USERNAME'), recipients=[to])
#     if is_txt:
#         msg.body = body
#     else:
#         msg.html = body
#     thr = Thread(target=send_mail_async, args=[app, msg])
#     thr.start()
#     return thr