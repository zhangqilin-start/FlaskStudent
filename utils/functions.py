import os


from flask import Flask

from views.admin import *
from App.models import db


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.register_blueprint(blueprint=admin, url_prefix='/user')




    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/flaskstudent'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 如果设置成True(默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它

    # 设置session密钥
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app=app)
    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
