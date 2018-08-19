# -*- coding: UTF-8 -*-

from app.models import Action, Role, roles_actions
from app.common.permission import permissions
from app.common.db import db


for permission in permissions:
    p = Action.query.filter_by(code=permission['action']).first()
    if not p:
        p = Action(
            name=permission['name'],
            action=permission['action']
        )
        db.session.add(p)
        db.session.commit()

role = Role.query.first()  # 这里默认获取一个角色，并且赋予权限
for p in Action.query.filter_by(status=1):
    r = db.session.query(roles_actions).join(Role).join(Action).\
        filter(
            Role.id == role.id,
            Role.status == 1,
            Action.id == p.id,
            Action.status == 1,
            roles_actions.status == 1,
        ).first()
    if not r:
        role.permissions.append(p)

role.save()