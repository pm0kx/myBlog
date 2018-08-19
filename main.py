#encoding: utf-8

from flask import Flask
from config import DevelopmentConfig

# from app.main import index
# from app.post import post


app = Flask(__name__)

# app.register_blueprint(index)
# app.register_blueprint(post)

# Import the views module
views = __import__('app.controllers.views')
#from app.controllers import views

app.config.from_object(DevelopmentConfig)


if __name__ == '__main__':
    app.run()
