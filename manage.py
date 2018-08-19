#encoding: utf-8

# import Flask Script object
#http://flask.pocoo.org/extensions/

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app.common.db import db
#from app import db,create_app
from app import create_app
from app import models

app = create_app('development' or 'default')


# Init manager object via app object
manager = Manager(app)

# Init migrate object via app and db object
migrate = Migrate(app, db)


# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("server", Server(host='127.0.0.1', port=8089))
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=app,
                db=db,
                User=models.User,
                Post=models.Post,
                Tag=models.Tag,
                Comment=models.Comment,
                Catalog=models.Catalog,
                Article=models.Article,
                Mail=models.Mail,
                Action=models.Mail,
                Resource=models.Resource,
                Group=models.Group,
                ActionLog=models.ActionLog,
                Attachment=models.Attachment,
                Server=Server
                )

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    manager.run()