

from flask import json,request

from app.common.time_util import get_localtime


from app.models import Action,ActionLog
from app.common.db import db


def action_log(req,act):
    request =req
    log =ActionLog(act)
    log.client_ip =request.remote_addr
    log.action_time =get_localtime()

    db.session.add(log)
    db.session.commit()